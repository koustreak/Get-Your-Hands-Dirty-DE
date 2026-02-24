# ─────────────────────────────────────────────
#  MySQL – Practice / Learning Environment
# ─────────────────────────────────────────────
FROM mysql:8.4

LABEL maintainer="practice-env"
LABEL description="MySQL instance for Get-Your-Hands-Dirty-DE practice"

# Practice credentials (NOT for production)
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=practice_db
ENV MYSQL_USER=dev
ENV MYSQL_PASSWORD=dev123

# Optional: drop any *.sql or *.sh init scripts in this dir
#   and they will be run automatically on first startup.
# COPY ./init/mysql/ /docker-entrypoint-initdb.d/

EXPOSE 3306
