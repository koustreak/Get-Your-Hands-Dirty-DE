# ─────────────────────────────────────────────
#  Neo4j – Practice / Learning Environment
# ─────────────────────────────────────────────
FROM neo4j:5

LABEL maintainer="practice-env"
LABEL description="Neo4j instance for Get-Your-Hands-Dirty-DE practice"

# Practice credentials (NOT for production)
ENV NEO4J_AUTH=neo4j/dev123

# APOC plugin is extremely useful for learning – enable it
ENV NEO4J_PLUGINS='["apoc"]'

# Accept the licence for the community edition (required from Neo4j 5+)
ENV NEO4J_server_memory_heap_initial__size=512m
ENV NEO4J_server_memory_heap_max__size=1g

# 7474 → HTTP browser
# 7687 → Bolt protocol (drivers)
EXPOSE 7474 7687
