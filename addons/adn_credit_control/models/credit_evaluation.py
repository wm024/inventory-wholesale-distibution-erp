from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AdnCreditEvaluation(models.Model):
    _name = "adn.credit.evaluation"
    _description = "Customer Credit Evaluation"
    _order = "evaluated_at desc, id desc"
    _check_company_auto = True

    name = fields.Char(required=True, default="New", index=True, readonly=True)
    credit_profile_id = fields.Many2one(
        "adn.partner.credit", required=True, ondelete="restrict", index=True,
        check_company=True, readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner", related="credit_profile_id.partner_id", store=True,
        index=True, readonly=True,
    )
    company_id = fields.Many2one(
        "res.company", required=True, index=True, readonly=True,
    )
    sale_order_id = fields.Many2one(
        "sale.order", ondelete="set null", index=True, check_company=True,
        readonly=True,
    )
    currency_id = fields.Many2one("res.currency", required=True, readonly=True)
    evaluated_at = fields.Datetime(
        required=True, default=fields.Datetime.now, index=True, readonly=True,
    )
    credit_limit = fields.Monetary(currency_field="currency_id", readonly=True)
    posted_ar_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    uninvoiced_order_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    overdue_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    overdue_1_30_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    overdue_over_30_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    exposure_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    available_credit = fields.Monetary(currency_field="currency_id", readonly=True)
    utilization_percentage = fields.Float(digits=(16, 4), readonly=True)
    decision = fields.Selection(
        [
            ("normal", "Normal"), ("warning", "Warning"),
            ("hold", "Hold"), ("blocked", "Blocked"),
        ], required=True, index=True, readonly=True,
    )
    hold_reasons = fields.Json(default=list, readonly=True)
    source_fingerprint = fields.Char(required=True, index=True, readonly=True)
    source_detail = fields.Json(readonly=True)
    approval_request_id = fields.Many2one(
        "adn.approval.request", ondelete="restrict", check_company=True,
        readonly=True,
    )
    released_at = fields.Datetime(readonly=True)
    released_by_id = fields.Many2one("res.users", readonly=True)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("adn.credit.evaluation") or "New"
                )
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.su:
            raise AccessError(_("Credit evaluation snapshots are system-managed and immutable."))
        return super().write(vals)

    def unlink(self):
        if not self.env.su:
            raise AccessError(_("Credit evaluation history cannot be deleted."))
        return super().unlink()


class AdnCreditService(models.AbstractModel):
    _name = "adn.credit.service"
    _description = "ADN Customer Credit Service"

    @api.model
    def _company_timezone(self, company):
        return company.partner_id.tz or "UTC"

    @api.model
    def _company_today(self, company):
        return fields.Date.context_today(self.with_context(tz=self._company_timezone(company)))

    @api.model
    def _order_conversion_date(self, order, company):
        if order.adn_credit_conversion_date:
            return order.adn_credit_conversion_date
        if order.date_order:
            localized = fields.Datetime.context_timestamp(
                order.with_context(tz=self._company_timezone(company)), order.date_order,
            )
            return localized.date()
        return self._company_today(company)

    @api.model
    def _lock_customer(self, partner):
        """Serialize credit-consuming confirmations for one commercial customer.

        The row lock is deliberately narrow and transaction-scoped. It prevents two
        concurrent confirmations from both reading the same available credit.
        """
        partner = partner.commercial_partner_id
        self.env.cr.execute(
            "SELECT id FROM res_partner WHERE id = %s FOR UPDATE",
            [partner.id],
        )
        partner.invalidate_recordset()

    @api.model
    def _get_credit_profile(self, partner, company):
        partner = partner.commercial_partner_id
        profile = self.env["adn.partner.credit"].sudo().search([
            ("commercial_partner_id", "=", partner.id),
            ("company_id", "=", company.id),
        ], limit=1)
        if not profile:
            profile = self.env["adn.partner.credit"].sudo().create({
                "partner_id": partner.id,
                "company_id": company.id,
            })
        return profile

    @api.model
    def _get_posted_receivables(self, partner, company):
        """Return posted customer invoice residuals in company currency.

        Unallocated customer credit notes are intentionally excluded per FSD.
        """
        lines = self.env["account.move.line"].sudo().search([
            ("company_id", "=", company.id),
            ("partner_id", "=", partner.commercial_partner_id.id),
            ("parent_state", "=", "posted"),
            ("account_id.account_type", "=", "asset_receivable"),
            ("move_id.move_type", "=", "out_invoice"),
            ("reconciled", "=", False),
            ("amount_residual", ">", 0),
        ])
        amount = sum(lines.mapped("amount_residual"))
        overdue_1_30 = 0.0
        overdue_over_30 = 0.0
        today = self._company_today(company)
        for line in lines:
            due_date = line.date_maturity or line.move_id.invoice_date_due
            if not due_date:
                continue
            overdue_days = (today - due_date).days
            bucket = self._overdue_bucket(overdue_days)
            if bucket == "warning":
                overdue_1_30 += line.amount_residual
            elif bucket == "hold":
                overdue_over_30 += line.amount_residual
        return amount, overdue_1_30, overdue_over_30, lines

    @api.model
    def _overdue_bucket(self, overdue_days):
        if 1 <= overdue_days <= 30:
            return "warning"
        if overdue_days > 30:
            return "hold"
        return "normal"

    @api.model
    def _get_uninvoiced_order_commitments(self, partner, company, exclude_order=None):
        if company.adn_credit_commitment_basis != "order_total_less_posted_invoice_lines":
            raise UserError(_(
                "Credit commitment basis is not configured for %s. Resolve DEC-006 with Finance "
                "and configure the company credit policy before confirming credit orders."
            ) % company.display_name)
        domain = [
            ("company_id", "=", company.id),
            ("partner_id.commercial_partner_id", "=", partner.commercial_partner_id.id),
            ("state", "=", "sale"),
        ]
        if exclude_order:
            domain.append(("id", "!=", exclude_order.id))
        orders = self.env["sale.order"].sudo().search(domain)
        total = 0.0
        detail = []
        orders.mapped("order_line.invoice_lines.move_id")
        for order in orders:
            amount, posted_invoice_amount = self._order_commitment_amount(order, company)
            total += amount
            detail.append({
                "order_id": order.id,
                "order_total_company_currency": order.currency_id._convert(
                    order.amount_total, company.currency_id, company,
                    self._order_conversion_date(order, company),
                ),
                "posted_invoice_lines_company_currency": posted_invoice_amount,
                "remaining_commitment_company_currency": amount,
            })
        return total, detail

    @api.model
    def _order_commitment_amount(self, order, company):
        """Order gross total less posted customer invoice lines linked to its SO lines.

        Line-level linkage handles invoices containing lines from multiple orders and avoids
        subtracting the whole invoice total from every linked order. Draft invoices and credit
        notes are not subtracted; posted AR remains the accounting source of record.
        """
        conversion_date = self._order_conversion_date(order, company)
        order_total = order.currency_id._convert(
            order.amount_total, company.currency_id, company, conversion_date,
        )
        invoice_lines = order.order_line.mapped("invoice_lines").filtered(
            lambda line: line.move_id.state == "posted"
            and line.move_id.move_type == "out_invoice"
            and line.display_type == "product"
        )
        for invoice_line in invoice_lines:
            linked_orders = invoice_line.sale_line_ids.mapped("order_id")
            if len(linked_orders) > 1:
                raise UserError(_(
                    "Posted invoice line %(line)s is linked to multiple sales orders. "
                    "Credit validation is blocked until Finance approves a "
                    "line-allocation resolver.",
                    line=invoice_line.display_name,
                ))
        posted_invoice_amount = sum(
            line.currency_id._convert(
                line.price_total, company.currency_id, company,
                line.move_id.date or self._company_today(company),
            )
            for line in invoice_lines
        )
        remaining = company.currency_id.round(order_total - posted_invoice_amount)
        return max(remaining, 0.0), posted_invoice_amount

    @api.model
    def _classify(self, exposure, limit_amount, overdue_1_30=0.0,
                  overdue_over_30=0.0, finance_blocked=False,
                  warning_at_80=False, hold_at_100=False):
        reasons = []
        if finance_blocked:
            return "blocked", ["customer_finance_blocked"]
        if overdue_over_30 > 0:
            reasons.append("invoice_overdue_more_than_30_days")
        if exposure > limit_amount or (
            hold_at_100 and limit_amount > 0 and exposure >= limit_amount
        ):
            reason = (
                "credit_exposure_at_or_over_100_percent"
                if hold_at_100 else "credit_exposure_over_100_percent"
            )
            reasons.append(reason)
        if reasons:
            return "hold", reasons
        warning_threshold_reached = limit_amount > 0 and (
            exposure > limit_amount * 0.80
            or (warning_at_80 and exposure >= limit_amount * 0.80)
        )
        if overdue_1_30 > 0 or warning_threshold_reached:
            if overdue_1_30 > 0:
                reasons.append("invoice_overdue_1_to_30_days")
            if warning_threshold_reached:
                reason = (
                    "credit_exposure_at_or_over_80_percent"
                    if warning_at_80 else "credit_exposure_over_80_percent"
                )
                reasons.append(reason)
            return "warning", reasons
        return "normal", reasons

    @api.model
    def _notify_approvers(self, request, company, body):
        group_ids = request.approver_group_ids.ids
        if not group_ids:
            return False
        users = self.env["res.users"].sudo().search([
            ("group_ids", "in", group_ids),
            ("company_ids", "in", company.id),
            ("active", "=", True),
            ("share", "=", False),
        ])
        request.message_post(
            body=body,
            partner_ids=sorted(set(users.mapped("partner_id").ids)),
        )
        return True

    @api.model
    def _idr_amount(self, company, amount):
        idr = self.env["res.currency"].search([("name", "=", "IDR")], limit=1)
        if not idr:
            raise ValidationError(_(
                "IDR currency is required to evaluate the approved credit thresholds."
            ))
        return idr._convert(amount, company.currency_id, company, self._company_today(company))

    @api.model
    def _evaluate(self, order, persist=True):
        partner = order.partner_id.commercial_partner_id
        company = order.company_id
        if not partner or not company:
            raise ValidationError(_("A customer and company are required for credit evaluation."))
        profile = self._get_credit_profile(partner, company)
        if not order.adn_credit_conversion_date:
            order.sudo().write({"adn_credit_conversion_date": self._company_today(company)})
        (
            posted_ar, overdue_1_30, overdue_over_30, invoice_lines
        ) = self._get_posted_receivables(partner, company)
        order_commitment, order_details = self._get_uninvoiced_order_commitments(
            partner, company, exclude_order=order,
        )
        current_order_amount, _posted_invoice_amount = self._order_commitment_amount(order, company)
        uninvoiced_total = order_commitment + current_order_amount
        exposure = posted_ar + uninvoiced_total
        limit_amount = profile.credit_limit
        available = limit_amount - exposure
        utilization = (
            exposure / limit_amount * 100.0
            if limit_amount > 0 else (100.0 if exposure > 0 else 0.0)
        )
        decision, reasons = self._classify(
            exposure, limit_amount, overdue_1_30, overdue_over_30,
            profile.finance_blocked,
            warning_at_80=company.adn_credit_warning_boundary == "at_80",
            hold_at_100=company.adn_credit_hold_boundary == "at_100",
        )
        receivable_details = []
        today = self._company_today(company)
        for line in invoice_lines:
            due_date = line.date_maturity or line.move_id.invoice_date_due
            overdue_days = (today - due_date).days if due_date else 0
            if overdue_days > 0:
                receivable_details.append({
                    "move_line_id": line.id,
                    "invoice_id": line.move_id.id,
                    "invoice_number": line.move_id.name,
                    "due_date": fields.Date.to_string(due_date) if due_date else False,
                    "overdue_days": overdue_days,
                    "residual_company_currency": line.amount_residual,
                })
        current_order_detail = {
            "order_id": order.id,
            "order_total_company_currency": company.currency_id._convert(
                order.amount_total, company.currency_id, company,
                self._order_conversion_date(order, company),
            ),
            "posted_invoice_lines_company_currency": _posted_invoice_amount,
            "remaining_commitment_company_currency": current_order_amount,
            "is_current_confirmation": True,
        }
        source_detail = {
            "receivables": receivable_details,
            "uninvoiced_orders": order_details + [current_order_detail],
        }
        source_snapshot = {
            "partner_id": partner.id,
            "company_id": company.id,
            "credit_limit": limit_amount,
            "posted_ar": posted_ar,
            "receivables": receivable_details,
            "uninvoiced_orders": order_details,
            "current_order_id": order.id,
            "current_order_amount": current_order_amount,
            "conversion_date": fields.Date.to_string(order.adn_credit_conversion_date),
            "overdue_1_30": overdue_1_30,
            "overdue_over_30": overdue_over_30,
            "finance_blocked": profile.finance_blocked,
            "commitment_basis": company.adn_credit_commitment_basis,
            "warning_boundary": company.adn_credit_warning_boundary,
            "hold_boundary": company.adn_credit_hold_boundary,
        }
        fingerprint = self.env["adn.approval.request"]._fingerprint(source_snapshot)
        evaluation = self.env["adn.credit.evaluation"]
        if persist:
            evaluation = evaluation.sudo().create({
                "credit_profile_id": profile.id,
                "company_id": company.id,
                "sale_order_id": order.id,
                "currency_id": company.currency_id.id,
                "credit_limit": limit_amount,
                "posted_ar_amount": posted_ar,
                "uninvoiced_order_amount": uninvoiced_total,
                "overdue_1_30_amount": overdue_1_30,
                "overdue_over_30_amount": overdue_over_30,
                "overdue_amount": overdue_1_30 + overdue_over_30,
                "exposure_amount": exposure,
                "available_credit": available,
                "utilization_percentage": utilization,
                "decision": decision,
                "hold_reasons": reasons,
                "source_fingerprint": fingerprint,
                "source_detail": source_detail,
            })
            profile.sudo().write({"status": decision})
            order.sudo().write({
                "adn_credit_evaluation_id": evaluation.id,
                "adn_credit_decision": decision,
                "adn_credit_exposure": exposure,
                "adn_credit_available": available,
                "adn_credit_utilization": utilization,
            })
        return {
            "profile": profile,
            "decision": decision,
            "exposure": exposure,
            "available": available,
            "limit": limit_amount,
            "over_limit": max(exposure - limit_amount, 0.0),
            "overdue_1_30": overdue_1_30,
            "overdue_over_30": overdue_over_30,
            "current_order_amount": current_order_amount,
            "snapshot": source_snapshot,
            "fingerprint": fingerprint,
            "evaluation": evaluation,
        }

    @api.model
    def _submit_exception(self, order, reason, result):
        if not reason or not reason.strip():
            raise ValidationError(_("A business justification is required for a credit exception."))
        hours = order.company_id.adn_credit_exception_validity_hours
        if hours <= 0:
            raise UserError(_(
                "Credit exception expiry is not configured. Resolve DEC-006 with Finance "
                "before enabling exception release."
            ))
        policy = self.env["adn.approval.policy"].get_active_policy(
            "CREDIT_EXCEPTION", order.company_id, "sale.order",
        )
        rules = policy.rule_ids.filtered("active")
        over_limit_threshold = self._idr_amount(order.company_id, 25000000.0)
        tier_code = (
            "CREDIT_FINANCE_MD"
            if result["over_limit"] > over_limit_threshold
            else "CREDIT_FINANCE_MANAGER"
        )
        rule = rules.filtered(lambda rec: rec.tier_code == tier_code)[:1]
        if not rule:
            raise ValidationError(_(
                "Credit exception policy is missing active rule '%s'." % tier_code
            ))
        approval_snapshot = order._adn_credit_exception_snapshot(result)
        request = self.env["adn.approval.request"]._submit_with_rule(
            "CREDIT_EXCEPTION", order, result["current_order_amount"], approval_snapshot,
            reason=reason, rule_override_id=rule.id,
            request_currency_id=order.company_id.currency_id.id,
        )
        request.sudo().write({
            "valid_until": fields.Datetime.add(fields.Datetime.now(), hours=hours),
        })
        order.sudo().write({"adn_credit_approval_request_id": request.id})
        result["evaluation"].sudo().write({"approval_request_id": request.id})
        self._notify_approvers(
            request, order.company_id,
            _("A customer credit exception requires your review."),
        )
        return request
