import hashlib
import json
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import AccessError, UserError, ValidationError


class AdnApprovalRequest(models.Model):
    _name = "adn.approval.request"
    _description = "ADN Approval Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "requested_at desc, id desc"

    name = fields.Char(required=True, copy=False, default="New", index=True, tracking=True)
    policy_id = fields.Many2one("adn.approval.policy", required=True, ondelete="restrict", index=True)
    policy_version = fields.Integer(required=True, readonly=True)
    company_id = fields.Many2one("res.company", required=True, index=True)
    source_model = fields.Char(required=True, index=True)
    source_res_id = fields.Integer(required=True, index=True)
    source_display_name = fields.Char(required=True)
    requester_id = fields.Many2one("res.users", required=True, readonly=True, default=lambda self: self.env.user)
    requested_at = fields.Datetime(required=True, readonly=True, default=fields.Datetime.now)
    reason = fields.Text()
    currency_id = fields.Many2one("res.currency")
    amount_basis = fields.Monetary(currency_field="currency_id")
    tier_code = fields.Char(required=True)
    approval_mode = fields.Selection([("all_required", "All Required"), ("any_required", "Any Required"), ("sequential", "Sequential")], required=True, default="sequential", readonly=True)
    sequence_mode = fields.Selection([("parallel", "Parallel"), ("ordered", "Ordered")], required=True, default="ordered", readonly=True)
    required_approvals = fields.Integer(required=True, default=1, readonly=True)
    state = fields.Selection([
        ("draft", "Draft"), ("submitted", "Submitted"), ("pending", "Pending Approval"),
        ("approved", "Approved"), ("rejected", "Rejected"), ("cancelled", "Cancelled"),
        ("superseded", "Superseded"),
    ], default="draft", required=True, tracking=True, index=True)
    source_fingerprint = fields.Char(required=True, readonly=True, index=True)
    source_snapshot = fields.Json(required=True, readonly=True)
    valid_until = fields.Datetime()
    submitted_by_id = fields.Many2one("res.users", readonly=True)
    completed_at = fields.Datetime(readonly=True)
    cancelled_at = fields.Datetime(readonly=True)
    step_ids = fields.One2many("adn.approval.step", "request_id", copy=False)
    item_ids = fields.One2many("adn.approval.item", "request_id", copy=False)
    event_ids = fields.One2many("adn.approval.event", "request_id", copy=False)
    approver_group_ids = fields.Many2many(
        "res.groups", compute="_compute_approver_group_ids", store=True,
        string="Routed Approver Groups",
    )
    step_count = fields.Integer(compute="_compute_counts")
    pending_step_count = fields.Integer(compute="_compute_counts")

    _sql_constraints = [
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("adn.approval.request") or "New"
        return super().create(vals_list)

    @api.depends("step_ids.approver_group_id")
    def _compute_approver_group_ids(self):
        for rec in self:
            rec.approver_group_ids = rec.step_ids.mapped("approver_group_id")

    @api.depends("step_ids", "step_ids.decision")
    def _compute_counts(self):
        for rec in self:
            rec.step_count = len(rec.step_ids)
            rec.pending_step_count = len(rec.step_ids.filtered(lambda s: s.decision == "pending"))

    @api.model
    def _fingerprint(self, snapshot):
        payload = json.dumps(snapshot, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @api.model
    def submit(self, policy_code, source_record, amount, snapshot, reason=None, item_values=None):
        """Create an amount-routed request; public RPC callers cannot select a rule."""
        return self._submit_with_rule(
            policy_code, source_record, amount, snapshot, reason=reason,
            item_values=item_values, rule_override_id=None, request_currency_id=None,
        )

    @api.model
    def _submit_with_rule(self, policy_code, source_record, amount, snapshot, reason=None,
                          item_values=None, rule_override_id=None, request_currency_id=None):
        """Internal adapter API for non-monetary routing such as line discount percentage."""
        if not source_record or not source_record.exists():
            raise ValidationError(_("The approval source record no longer exists."))
        source_record.check_access("read")
        company = (source_record.company_id if "company_id" in source_record._fields else False) or self.env.company
        policy = self.env["adn.approval.policy"].get_active_policy(policy_code, company, source_record._name)
        policy.ensure_one()
        rules = policy.rule_ids.filtered("active").sorted(lambda r: (r.sequence, r.id))
        if rule_override_id:
            rule = self.env["adn.approval.rule"].browse(rule_override_id).exists()
            if not rule or rule.policy_id != policy or not rule.active:
                raise ValidationError(_("The selected approval rule does not belong to the active policy."))
        else:
            matching = rules.filtered(lambda r: r.matches_amount(amount))
            if not matching:
                raise ValidationError(_("No approval rule matches amount %s for policy %s.") % (amount, policy.code))
            # A single matching tier is expected; overlapping ranges are configuration errors.
            if len(matching) > 1:
                raise ValidationError(_("Approval policy '%s' has overlapping amount rules.") % policy.code)
            rule = matching[0]
        if not rule.approver_group_ids:
            raise ValidationError(_("The selected approval rule has no approver groups."))
        user = self.env.user
        excluded = rule.requester_group_exclusions & user.groups_id
        steps_data = []
        for group in rule.approver_group_ids:
            if group in excluded:
                continue
            for approval_no in range(rule.required_approvals):
                steps_data.append({"sequence": len(steps_data) + 1, "approver_group_id": group.id})
        if not steps_data:
            raise ValidationError(_("No eligible approver groups remain after requester exclusions."))
        fingerprint = self._fingerprint(snapshot)
        duplicate = self.search([("policy_id", "=", policy.id), ("source_model", "=", source_record._name), ("source_res_id", "=", source_record.id), ("source_fingerprint", "=", fingerprint), ("state", "in", ["pending", "approved"])], limit=1)
        if duplicate:
            raise ValidationError(_("An active or approved request already exists for this source version."))
        if not policy.rule_ids.filtered("active"):
            raise ValidationError(_("The selected approval policy has no active rules."))
        request = self.create({
            "policy_id": policy.id, "policy_version": policy.policy_version,
            "company_id": company.id, "source_model": source_record._name,
            "source_res_id": source_record.id, "source_display_name": source_record.display_name,
            "requester_id": user.id, "reason": reason, "currency_id": request_currency_id or policy.currency_id.id,
            "amount_basis": amount, "tier_code": rule.tier_code,
            "approval_mode": policy.approval_mode, "sequence_mode": rule.sequence_mode,
            "required_approvals": rule.required_approvals,
            "source_fingerprint": fingerprint, "source_snapshot": snapshot,
            "submitted_by_id": user.id, "state": "pending",
            "step_ids": [(0, 0, vals) for vals in steps_data],
            "item_ids": [(0, 0, vals) for vals in (item_values or [])],
        })
        request._append_event("submit", "draft", "pending", reason)
        if policy.approval_mode == "any_required":
            request.message_post(body=_("Any one authorized approver may approve this request."))
        return request

    def _append_event(self, event_type, previous_state=None, new_state=None, comment=None, payload=None):
        for rec in self:
            self.env["adn.approval.event"].create({
                "request_id": rec.id, "event_type": event_type,
                "actor_id": self.env.user.id, "previous_state": previous_state or "",
                "new_state": new_state or rec.state, "comment": comment or "",
                "payload_snapshot": payload or {},
            })

    def _check_actor(self, step):
        self.ensure_one()
        user = self.env.user
        if user.id == self.requester_id.id:
            raise AccessError(_("The requester cannot approve their own request."))
        if self.step_ids.filtered(lambda s: s.decided_by_id == user and s.id != step.id):
            raise AccessError(_("Each approval step must be approved by a distinct user."))
        if step.approver_id and step.approver_id != user:
            raise AccessError(_("This approval step is assigned to another user."))
        if step.approver_group_id not in user.groups_id:
            raise AccessError(_("You are not a member of the required approver group."))
        if user.company_ids and self.company_id not in user.company_ids:
            raise AccessError(_("You are not authorized for this company."))

    def action_approve(self, comment=None):
        for request in self:
            if request.state != "pending":
                raise UserError(_("Only pending requests can be approved."))
            pending_steps = request.step_ids.filtered(lambda s: s.decision == "pending").sorted(lambda s: (s.sequence, s.id))
            if request.sequence_mode == "ordered":
                first_step = pending_steps[:1]
                step = first_step.filtered(lambda s: s.approver_group_id in self.env.user.groups_id)
            else:
                step = pending_steps.filtered(lambda s: s.approver_group_id in self.env.user.groups_id)[:1]
            if not step:
                raise AccessError(_("There is no pending approval step assigned to one of your groups."))
            step._record_decision("approved", comment=comment)
            approved_count = len(request.step_ids.filtered(lambda s: s.decision == "approved"))
            complete = (approved_count >= request.required_approvals) if request.approval_mode == "any_required" else not request.step_ids.filtered(lambda s: s.decision == "pending")
            if complete:
                for remaining in request.step_ids.filtered(lambda s: s.decision == "pending"):
                    remaining.sudo().write({"decision": "skipped"})
                old = request.state
                request.sudo().write({"state": "approved", "completed_at": fields.Datetime.now()})
                request._append_event("approve", old, "approved", comment)
            else:
                request._append_event("approve", "pending", "pending", comment, {"step_id": step.id})
        return True

    def action_reject(self, reason):
        if not reason or not reason.strip():
            raise ValidationError(_("A rejection reason is mandatory."))
        for request in self:
            if request.state != "pending":
                raise UserError(_("Only pending requests can be rejected."))
            step = request.step_ids.filtered(lambda s: s.decision == "pending").sorted(lambda s: (s.sequence, s.id))[:1]
            if not step:
                raise UserError(_("There is no pending approval step."))
            step._record_decision("rejected", comment=reason)
            request.sudo().write({"state": "rejected", "completed_at": fields.Datetime.now()})
            request._append_event("reject", "pending", "rejected", reason, {"step_id": step.id})
        return True

    def action_cancel(self, reason=None):
        if not self.env.user.has_group("adn_approval_core.group_approval_manager") and not self.env.user.has_group("base.group_system"):
            raise AccessError(_("Only an Approval Manager may cancel an approval request."))
        for request in self:
            if request.state not in ("draft", "submitted", "pending"):
                raise UserError(_("This request can no longer be cancelled."))
            old = request.state
            request.sudo().write({"state": "cancelled", "cancelled_at": fields.Datetime.now()})
            request._append_event("cancel", old, "cancelled", reason)
        return True

    def action_supersede(self, new_snapshot, reason=None):
        for request in self:
            if request.state not in ("pending", "approved"):
                continue
            source = self.env[request.source_model].browse(request.source_res_id).exists()
            if not source:
                raise ValidationError(_("The approval source record no longer exists."))
            source.check_access("write")
            if request._fingerprint(new_snapshot) == request.source_fingerprint:
                raise ValidationError(_("The source fingerprint has not changed; this request cannot be superseded."))
            old = request.state
            request.sudo().write({"state": "superseded"})
            request._append_event("supersede", old, "superseded", reason, {
                "old_fingerprint": request.source_fingerprint,
                "new_fingerprint": self._fingerprint(new_snapshot),
            })
        return True

    def assert_released(self, source_record, policy_code, snapshot):
        self.ensure_one()
        if self.state != "approved":
            raise UserError(_("The transaction cannot proceed: approval is not complete."))
        if self.source_model != source_record._name or self.source_res_id != source_record.id:
            raise ValidationError(_("The approval request does not belong to this source transaction."))
        if self.source_fingerprint != self._fingerprint(snapshot):
            raise UserError(_("Approval is no longer valid because approval-relevant source values changed."))
        if self.policy_id.code != policy_code:
            raise ValidationError(_("The approval request uses a different policy."))
        return True

    def write(self, vals):
        protected = {"policy_id", "policy_version", "company_id", "source_model", "source_res_id", "requester_id", "requested_at", "source_fingerprint", "source_snapshot", "state", "completed_at", "cancelled_at"}
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("Approval lifecycle fields can only be changed through workflow actions."))
        return super().write(vals)

    def unlink(self):
        if not self.env.user.has_group("adn_approval_core.group_approval_manager") and not self.env.su:
            raise AccessError(_("Approval requests cannot be deleted by business users."))
        if any(rec.state not in ("draft", "cancelled") for rec in self):
            raise UserError(_("Only draft or cancelled requests may be deleted by an Approval Manager."))
        return super().unlink()
