![CI](https://github.com/H9m8/idp-pipeline/actions/workflows/ci.yml/badge.svg)

# IDP Pipeline — Intelligent Document Processing

An AI-powered pipeline that ingests PDF invoices, extracts structured data with an
LLM, validates it, detects anomalies and duplicates using vector similarity (RAG),
stores everything in a cloud Postgres database, and answers natural-language
questions about the data through an autonomous agent with tool calling and memory.

## What it demonstrates
- **AI agents & tool calling** — an agent that writes its own SQL and chooses tools
- **Structured extraction** — forced-JSON output from unstructured PDFs
- **RAG** — embeddings in pgvector for semantic duplicate detection
- **Validation** — deterministic checks that catch LLM errors, with a tested module
- **Cloud + database** — Supabase Postgres with pgvector
- **CI/CD** — GitHub Actions running tests on every push
- **Orchestration** — n8n workflows for the whole pipeline

## Architecture
Two sides:
1. **Ingestion** — Upload -> extract text -> LLM extraction -> validation -> embedding
   -> duplicate detection -> store across relational tables.
2. **Query** — A chat agent with a SQL tool, a search tool, and persistent memory
   answers questions like "what's my total spend with vendor X?"

See `docs/architecture.svg` for the full diagram.

## Stack
n8n - OpenAI - Supabase (Postgres + pgvector) - Python - GitHub Actions

## Database
The full schema (5 tables + the vector search function) is in `db/schema.sql`.
Generate synthetic test invoices with `python db/seed_synthetic.py`.

## Tests
    cd code && python -m pytest -v

## Workflows
Exported n8n workflows are in `workflows/`:
- `01_intake.json` — upload endpoint
- `02_extract_phase_4.json` — extraction, validation, RAG, duplicate detection
- `03_query_agent.json` — natural-language query agent

## Status
- [x] Phase 0 — environment & accounts
- [x] Phase 1 — schema & intake
- [x] Phase 2 — extraction agent
- [x] Phase 3 — validation & tests
- [x] Phase 4 — RAG & duplicate detection
- [x] Phase 5 — NL query agent
- [x] Phase 6 — CI/CD & docs
