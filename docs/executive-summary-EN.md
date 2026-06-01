# Executive Summary — Néovolt Grid+

**Prepared for:** Néovolt Steering Committee · **By:** cross-functional project team · **Scope:** one-week framing & prototyping sprint

## Context
Néovolt, a regional energy distributor serving ~600,000 delivery points, operates **critical
infrastructure** but under-exploits the flood of data from its smart meters: siloed databases,
uneven quality, late fraud detection, no decision dashboards, an un-audited security posture,
and no overall governance. The **Néovolt Grid+** programme aims to fix this. We were asked
not for a production system, but for a **credible prototype and a decision file**.

## What we delivered
A working, end-to-end prototype covering the full chain, plus the management framing:

- **Data platform (engineering):** an ingestion-and-quality pipeline turning raw, imperfect
  meter readings into clean data (**98.5% usable** after de-duplication and anomaly handling),
  a relational warehouse, and a **REST API** — all containerised with Docker and tested.
- **Fraud/anomaly detection (data science):** an unsupervised model that, by investigating only
  **5% of meters, surfaces 54% of known frauds** (lift **×10.8** over random) — with an
  explainable reason per alert and a human kept in the loop.
- **Decision analytics:** interactive dashboards for network, finance and customer-relations
  leaders, plus text mining of 3,000 complaints (satisfaction **2.45/5**; billing is the top pain point).
- **Security & compliance:** a SIEM analysis that uncovered a **real attack** in the logs (an
  external IP brute-forced and compromised a data-exporting account), an EBIOS risk map, a
  DevSecOps dependency audit (3 CVEs found and fixed), and an NIS 2 incident runbook.
- **Management:** a **business case within the €450k envelope** (€325k, €125k margin), an
  estimated **€5.7M/year fraud loss pool** (~€2.3M recoverable in year one), a **payback of
  ~1.7 months**, plus governance (RACI), risk and change-management plans.

## Key recommendation
**Detect fraud first, forecast demand second.** Fraud delivers a fast, measurable return that
self-funds the rest; demand forecasting (avoided balancing-energy costs) follows in phase 2.
**Security is a phase-0 gate, not an afterthought** — multi-factor authentication and a SIEM
must precede go-live, given critical infrastructure and personal data.

## Why it is trustworthy
Every figure is grounded in the supplied data, assumptions are explicit and adjustable,
limitations are stated, and **privacy and security are built in by design** (data minimisation,
no personal data in the code repository, human-in-the-loop fraud decisions, a DPIA for the
fraud model). The prototype is fully reproducible from the documentation.

**Bottom line:** a low-risk, high-return first step is ready. We recommend the committee
approve phase 1 to industrialise fraud detection and the data platform, with security as a
blocking milestone.
