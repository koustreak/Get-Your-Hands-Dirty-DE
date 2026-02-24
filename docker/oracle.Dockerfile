# ─────────────────────────────────────────────
#  Oracle XE – Practice / Learning Environment
#  Using gvenzl/oracle-xe (free, lighter Oracle
#  image suitable for development/learning)
# ─────────────────────────────────────────────
FROM gvenzl/oracle-xe:21-slim

LABEL maintainer="practice-env"
LABEL description="Oracle XE instance for Get-Your-Hands-Dirty-DE practice"

# Practice credentials (NOT for production)
# ORACLE_PASSWORD sets the SYS / SYSTEM / PDBADMIN password
ENV ORACLE_PASSWORD=dev123
ENV ORACLE_DATABASE=PRACTICE

# Optional: place any *.sql init scripts here to run on first startup
# COPY ./init/oracle/ /container-entrypoint-initdb.d/

# 1521 → Oracle listener
# 5500 → Oracle Enterprise Manager (optional)
EXPOSE 1521 5500
