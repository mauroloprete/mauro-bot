# SoporteBot

Agente RAG con memoria desplegado con **Declarative Automation Bundles (DABs)**.

Ejemplo de la charla *"De YAML a producción"* — Databricks Meetup Uruguay, junio 2026.

## Arquitectura

```
Usuario → Databricks App (Streamlit) → Serving Endpoint → Vector Search
                                              ↕
                                     Lakebase (memoria)
```

**Un solo `databricks.yml` despliega todo:**

- MLflow Experiment + Registered Model
- Serving Endpoint con AI Gateway (rate limits + guardrails PII)
- Lakebase PostgreSQL (memoria short/long-term)
- Databricks App (chat UI con Streamlit)
- Job de refresh del Vector Search Index
- Permisos y service principal

## Requisitos

- Databricks CLI >= 0.230
- Workspace con Unity Catalog, Vector Search y Lakebase habilitados

## Uso

```bash
# 1. Clonar
git clone <repo-url> && cd soporte-bot

# 2. Configurar
#    Editá databricks.yml → workspace hosts, catalog names, service principal

# 3. Validar
databricks bundle validate -t dev

# 4. Ver qué va a crear
databricks bundle plan -t dev

# 5. Deployar
databricks bundle deploy -t dev

# 6. Abrir la app
databricks bundle open chat_ui -t dev
```

## Estructura

```
soporte-bot/
├── databricks.yml           # Todo el deploy
├── src/
│   ├── agent.py             # Agente RAG (MLflow PythonModel)
│   └── refresh_index.py     # Job: sync Vector Search
├── app/
│   ├── app.py               # Streamlit chat UI
│   └── requirements.txt
└── .github/
    └── workflows/
        └── deploy.yml       # CI/CD con GitHub Actions
```

## Links

- [Documentacion DABs](https://docs.databricks.com/aws/en/dev-tools/bundles)
- [Lakebase con DABs](https://learn.microsoft.com/en-us/azure/databricks/oltp/projects/manage-with-bundles)
- [Agent memory con Lakebase](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/agent-framework/stateful-agents)
- [Blog: Spark de Ideas](https://mauroloprete.github.io/mauroloprete/)
