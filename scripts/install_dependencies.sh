
#!/usr/bin/env bash

# ============================================================
# ADN ERP - Dependency Installation Script
# Project : PT Arunika Distribusi Nusantara
# Project ID: ADN-ERP-2026-001
# Platform: Odoo 19 Enterprise
# OS      : Ubuntu Linux
# Database: PostgreSQL
#
# Usage:
#   sudo bash scripts/install_dependencies.sh
#
# Optional environment variables:
#   ODOO_USER=odoo
#   ODOO_HOME=/opt/odoo
#   ODOO_SRC=/opt/odoo/odoo
#   ODOO_VENV=/opt/odoo/venv
# ============================================================

set -Eeuo pipefail

# ------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------

ODOO_USER="${ODOO_USER:-odoo}"
ODOO_HOME="${ODOO_HOME:-/opt/odoo}"
ODOO_SRC="${ODOO_SRC:-${ODOO_HOME}/odoo}"
ODOO_VENV="${ODOO_VENV:-${ODOO_HOME}/venv}"

LOG_PREFIX="[ADN-ERP-SETUP]"

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

trap 'error "Installation failed at line ${LINENO}. Check the output above."' ERR

# ------------------------------------------------------------
# 4. PRE-INSTALLATION VALIDATION
# ------------------------------------------------------------

if [[ "${EUID}" -ne 0 ]]; then
    error "Please execute this script with sudo or as root."
fi

if [[ ! -f /etc/os-release ]]; then
    error "Cannot identify operating system."
fi

source /etc/os-release

if [[ "${ID}" != "ubuntu" ]]; then
    error "This script is designed for Ubuntu Linux."
fi

if [[ ! -f "${ODOO_SRC}/requirements.txt" ]]; then
    error "Odoo requirements.txt not found at ${ODOO_SRC}."
    error "Clone or place the Odoo source code before running this script."
fi

log "Starting dependency installation..."
log "Ubuntu version: ${VERSION_ID}"
log "Odoo source: ${ODOO_SRC}"
log "Python environment: ${ODOO_VENV}"

# ------------------------------------------------------------
# 5. SYSTEM UPDATE
# ------------------------------------------------------------

log "Updating Ubuntu package index..."

export DEBIAN_FRONTEND=noninteractive

apt-get update

# ------------------------------------------------------------
# 6. SYSTEM DEPENDENCIES
# ------------------------------------------------------------

log "Installing system dependencies..."

apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    gnupg \
    lsb-release \
    software-properties-common \
    build-essential \
    pkg-config \
    gcc \
    g++ \
    make \
    python3 \
    python3-dev \
    python3-venv \
    python3-pip \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    libfreetype6-dev \
    postgresql \
    postgresql-client

# ------------------------------------------------------------
# 7. POSTGRESQL SERVICE
# ------------------------------------------------------------

log "Enabling PostgreSQL service..."

systemctl enable postgresql
systemctl start postgresql

if ! systemctl is-active --quiet postgresql; then
    error "PostgreSQL service is not running."
fi

log "PostgreSQL service is running."

# ------------------------------------------------------------
# 8. CREATE ODOO SYSTEM USER
# ------------------------------------------------------------

log "Checking Odoo system user..."

if ! id "${ODOO_USER}" >/dev/null 2>&1; then
    useradd \
        --system \
        --create-home \
        --home-dir /var/lib/odoo \
        --shell /usr/sbin/nologin \
        "${ODOO_USER}"

    log "Created system user: ${ODOO_USER}"
else
    log "System user already exists: ${ODOO_USER}"
fi

# ------------------------------------------------------------
# 9. CREATE REQUIRED DIRECTORIES
# ------------------------------------------------------------

log "Creating Odoo directories..."

mkdir -p \
    "${ODOO_HOME}" \
    "${ODOO_VENV}" \
    /var/lib/odoo \
    /var/log/odoo \
    /etc/odoo

chown -R "${ODOO_USER}:${ODOO_USER}" \
    /var/lib/odoo \
    /var/log/odoo

# ------------------------------------------------------------
# 10. CREATE PYTHON VIRTUAL ENVIRONMENT
# ------------------------------------------------------------

log "Creating Python virtual environment..."

if [[ ! -d "${ODOO_VENV}/bin" ]]; then
    python3 -m venv "${ODOO_VENV}"
fi

# ------------------------------------------------------------
# 11. INSTALL PYTHON BUILD TOOLS
# ------------------------------------------------------------

log "Upgrading Python packaging tools..."

"${ODOO_VENV}/bin/python" -m pip install \
    --upgrade \
    pip \
    setuptools \
    wheel

# ------------------------------------------------------------
# 12. INSTALL ODOO PYTHON REQUIREMENTS
# ------------------------------------------------------------

log "Installing Odoo Python dependencies..."

"${ODOO_VENV}/bin/python" -m pip install \
    --requirement "${ODOO_SRC}/requirements.txt"

# ------------------------------------------------------------
# 13. SET PERMISSIONS
# ------------------------------------------------------------

log "Setting Odoo directory ownership..."

chown -R "${ODOO_USER}:${ODOO_USER}" "${ODOO_VENV}"

# ------------------------------------------------------------
# 14. VERIFY INSTALLATION
# ------------------------------------------------------------

log "Verifying Python environment..."

"${ODOO_VENV}/bin/python" --version

"${ODOO_VENV}/bin/python" -m pip check

log "Verifying PostgreSQL..."

psql --version

# ------------------------------------------------------------
# 15. INSTALLATION SUMMARY
# ------------------------------------------------------------

echo
echo "============================================================"
echo " ADN ERP DEPENDENCY INSTALLATION COMPLETED"
echo "============================================================"
echo " Odoo User       : ${ODOO_USER}"
echo " Odoo Home       : ${ODOO_HOME}"
echo " Odoo Source     : ${ODOO_SRC}"
echo " Python Venv     : ${ODOO_VENV}"
echo " Python          : $("${ODOO_VENV}/bin/python" --version)"
echo " PostgreSQL      : $(psql --version)"
echo "============================================================"
echo
echo " NEXT STEPS:"
echo " 1. Configure PostgreSQL database role and permissions."
echo " 2. Configure /etc/odoo/odoo.conf."
echo " 3. Verify Enterprise addons path and access permissions."
echo " 4. Configure the Odoo systemd service."
echo " 5. Configure reverse proxy and HTTPS."
echo " 6. Install standard Odoo applications and ADN custom addons."
echo
echo " IMPORTANT:"
echo " Pin and verify Ubuntu, Python, PostgreSQL and Odoo versions"
echo " against the approved deployment environment before production."
echo "============================================================"
