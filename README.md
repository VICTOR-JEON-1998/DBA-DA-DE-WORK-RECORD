# Data Infrastructure Engineering Notes

Real-world case studies and technical notes spanning **DBA (MSSQL/PostgreSQL) → Data Analytics → Data Engineering**, built from hands-on production work and self-directed study in cloud/AI data infrastructure.

> 👉 **Start here:**
> - [`DBA_note/`](./DBA_note) — performance tuning & troubleshooting case studies
> - [`Pgvector/`](./Pgvector) — vector search implementation & indexing strategy
> - [`DE_note/`](./DE_note) — pipeline & automation work

---

## Highlights

- 🔧 **[Case: Query performance improved via index redesign — Xs → Ys]** ([DBA_note](./DBA_note))
- 📊 **[Case: ETL pipeline built for Z, reducing manual reporting time by N%]** ([DA_note](./DA_note) / [DE](./DE))
- 🧠 **[pgvector: HNSW vs IVFFlat indexing benchmark at scale]** ([Pgvector](./Pgvector))
- ⚙️ **[Automation: recurring DBA task automated with N hours/week saved]** ([Automation](./Automation))

*(위 4개는 실제 케이스 제목/수치로 교체 필요 — 지금은 자리표시자)*

---

## Background

MSSQL DBA (2+ years) with hands-on experience across database operations, data analysis, and ETL pipelines. Currently expanding into PostgreSQL, vector search (pgvector/RAG), and cloud-native data infrastructure — background in AI (AI Convergence major) informs the theory side of this transition.

This repo tracks that expansion: production DBA work on one end, applied AI-data infrastructure experiments on the other.

---

## Repository Structure

| Folder | Area | What's inside |
|---|---|---|
| [`DBA_note/`](./DBA_note) | DBA | Tuning & troubleshooting case studies (MSSQL, expanding to PostgreSQL) |
| [`DA_note/`](./DA_note) | Data Analysis | Analysis work, reporting logic |
| [`DE/`](./DE) · [`DE_note/`](./DE_note) | Data Engineering | Pipeline design, ETL work, Airflow |
| [`Pgvector/`](./Pgvector) | AI Infra | pgvector implementation, indexing/tuning experiments |
| [`RAG/`](./RAG) | AI Infra | Retrieval-augmented generation experiments |
| [`Automation/`](./Automation) | Ops | Scripts automating recurring DBA/ops tasks |
| [`scripts/`](./scripts) · [`templates/`](./templates) | Utility | Reusable scripts & templates |
| [`work_record/`](./work_record) | Log | On-the-job work log (ongoing) |

Each case study follows: **Context → Problem (with numbers) → Approach → Result (with numbers) → What I'd do differently.**

---

## Connect

- Blog: *(추가 예정)*
- LinkedIn: *(추가 예정)*
