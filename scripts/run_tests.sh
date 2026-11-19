
#!/usr/bin/env bash

# ============================================================
# ADN ERP - Automated Test Runner
# Project    : PT Arunika Distribusi Nusantara
# Project ID : ADN-ERP-2026-001
# Platform   : Odoo 19 Enterprise
# Database   : PostgreSQL
#
# Usage:
#   ./scripts/run_tests.sh
#
# Optional environment variables:
#   ODOO_BIN=/opt/odoo/odoo/odoo-bin
#   ODOO_CONFIG=/etc/odoo/odoo.conf
#   ODOO_VENV=/opt/odoo/venv
#   ODOO_TEST_DB=adn_erp_test
#   TEST_ACTION=update
#   TEST_TAGS=+standard
#   TEST_MODULES="adn_approval_core adn_purchase_approval"
#   TEST_LOG_DIR=./logs/tests
# ============================================================

set -Eeuo pipefail

# ------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------

ODOO_HOME="${ODOO_HOME:-/opt/odoo}"

ODOO_BIN="${ODOO_BIN:-${ODOO_HOME}/odoo/odoo-bin}"
ODOO_CONFIG="${ODOO_CONFIG:-/etc/odoo/odoo.conf}"
ODOO_VENV="${ODOO_VENV:-${ODOO_HOME}/venv}"

PYTHON_BIN="${ODOO_VENV}/bin/python"

ODOO_TEST_DB="${ODOO_TEST_DB:-adn_erp_test}"

TEST_ACTION="${TEST_ACTION:-update}"
TEST_TAGS="${TEST_TAGS:-+standard}"

TEST_MODULES="${TEST_MODULES:-\
adn_approval_core \
adn_purchase_approval \
adn_sale_discount_approval \
adn_credit_control \
adn_inventory_adjustment_approval \
adn_refund_approval \
adn_vendor_scorecard}"

TEST_LOG_DIR="${TEST_LOG_DIR:-./logs/tests}"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
TEST_LOG="${TEST_LOG_DIR}/odoo_tests_${TIMESTAMP}.log"

LOG_PREFIX="[ADN-ERP-TEST]"

# ------------------------------------------------------------
# 2. LOGGING
# ------------------------------------------------------------

log() {
    echo "${LOG_PREFIX} $1"
}

error() {
    echo "${LOG_PREFIX} ERROR: $1" >&2
    exit 1
}

# ------------------------------------------------------------
# 3. ERROR HANDLING
# ------------------------------------------------------------

trap 'error "Test execution failed at line ${LINENO}. Check the test log: ${TEST_LOG}"' ERR

# ------------------------------------------------------------
# 4. VALIDATION
# ------------------------------------------------------------

log "Validating test environment..."

[[ -f "${ODOO_BIN}" ]] || error "Odoo executable not found: ${ODOO_BIN}"
[[ -f "${ODOO_CONFIG}" ]] || error "Odoo config not found: ${ODOO_CONFIG}"
[[ -x "${PYTHON_BIN}" ]] || error "Python virtual environment not found: ${PYTHON_BIN}"

if [[ -z "${ODOO_TEST_DB// /}" ]]; then
    error "ODOO_TEST_DB must not be empty."
fi

# Prevent accidental execution against an obviously named
# production database.
if [[ "${ODOO_TEST_DB,,}" =~ (prod|production|live) ]]; then
    error "Production-like database name detected. Tests are blocked."
fi

case "${TEST_ACTION}" in
    install|update)
        ;;
    *)
        error "TEST_ACTION must be either 'install' or 'update'."
        ;;
esac

# ------------------------------------------------------------
# 5. PREPARE TEST MODULES
# ------------------------------------------------------------

read -r -a MODULE_ARRAY <<< "${TEST_MODULES}"

if [[ "${#MODULE_ARRAY[@]}" -eq 0 ]]; then
    error "No test modules configured."
fi

MODULES_CSV="$(IFS=,; echo "${MODULE_ARRAY[*]}")"

mkdir -p "${TEST_LOG_DIR}"

log "Test database : ${ODOO_TEST_DB}"
log "Test action   : ${TEST_ACTION}"
log "Test tags     : ${TEST_TAGS}"
log "Test modules  : ${MODULES_CSV}"
log "Test log      : ${TEST_LOG}"

# ------------------------------------------------------------
# 6. BUILD ODOO COMMAND
# ------------------------------------------------------------

ODOO_ARGS=(
    "${PYTHON_BIN}"
    "${ODOO_BIN}"
    "--config=${ODOO_CONFIG}"
    "--database=${ODOO_TEST_DB}"
    "--test-enable"
    "--test-tags=${TEST_TAGS}"
    "--stop-after-init"
    "--workers=0"
    "--max-cron-threads=0"
    "--log-level=test"
    "--logfile=${TEST_LOG}"
)

case "${TEST_ACTION}" in
    install)
        ODOO_ARGS+=("--init=${MODULES_CSV}")
        ;;
    update)
        ODOO_ARGS+=("--update=${MODULES_CSV}")
        ;;
esac

# ------------------------------------------------------------
# 7. EXECUTE TESTS
# ------------------------------------------------------------

log "Starting Odoo automated tests..."

START_TIME="$(date +%s)"

set +e

"${ODOO_ARGS[@]}" 2>&1 | tee -a "${TEST_LOG}"

TEST_EXIT_CODE="${PIPESTATUS[0]}"

set -e

END_TIME="$(date +%s)"
DURATION="$((END_TIME - START_TIME))"

# ------------------------------------------------------------
# 8. TEST RESULT
# ------------------------------------------------------------

echo
echo "============================================================"

if [[ "${TEST_EXIT_CODE}" -eq 0 ]]; then
    echo " ADN ERP AUTOMATED TESTS: PASSED"
    log "All selected Odoo test executions completed successfully."
else
    echo " ADN ERP AUTOMATED TESTS: FAILED"
    log "Odoo returned exit code: ${TEST_EXIT_CODE}"
fi

echo "============================================================"
echo " Database      : ${ODOO_TEST_DB}"
echo " Action        : ${TEST_ACTION}"
echo " Modules       : ${MODULES_CSV}"
echo " Duration      : ${DURATION} seconds"
echo " Exit Code     : ${TEST_EXIT_CODE}"
echo " Log File      : ${TEST_LOG}"
echo "============================================================"

exit "${TEST_EXIT_CODE}"
