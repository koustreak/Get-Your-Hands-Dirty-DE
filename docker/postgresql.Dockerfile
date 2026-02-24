# ─────────────────────────────────────────────
#  PostgreSQL – Practice / Learning Environment
# ─────────────────────────────────────────────
FROM postgres:16

LABEL maintainer="practice-env"
LABEL description="PostgreSQL instance for Get-Your-Hands-Dirty-DE practice"

# Practice credentials (NOT for production)
ENV POSTGRES_USER=dev
ENV POSTGRES_PASSWORD=dev123
ENV POSTGRES_DB=practice_db

# Optional: drop any *.sql or *.sh init scripts in this dir
#   and they will be run automatically on first startup.
# COPY ./init/postgresql/ /docker-entrypoint-initdb.d/

EXPOSE 5432
