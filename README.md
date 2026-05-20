# IDP Pipeline — Intelligent Document Processing

An AI-powered pipeline that ingests PDFs (invoices/receipts), extracts
structured data via an LLM agent with tool calling, validates and
flags anomalies using RAG, stores everything in Postgres + pgvector,
and answers natural-language questions about the data.

## Stack
n8n · OpenAI · Supabase (Postgres + pgvector) · GitHub Actions

## Status
- [x] Phase 0 — environment & accounts
- [x] Phase 1 — schema & intake webhook
- [x] Phase 2 — extraction agent
- [ ] Phase 3 — validation & tests
- [ ] Phase 4 — RAG & anomaly detection
- [ ] Phase 5 — natural language query agent
- [ ] Phase 6 — CI/CD & repo polish
