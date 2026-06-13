# Databricks notebook source
# MAGIC %md
# MAGIC # Refresh Vector Search Index
# MAGIC Sincroniza la tabla de documentos con el índice de Vector Search.

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

w.vector_search_indexes.sync_index(
    index_name="dev_catalog.agents.soporte_bot_vs_index"
)

print("Index sync triggered.")
