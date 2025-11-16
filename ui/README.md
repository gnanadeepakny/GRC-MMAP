# Project GRC-MMAP: Multi-Framework Mapping & Automation Platform

**GRC-MMAP** is a scalable, containerized Governance, Risk, and Compliance (GRC) prototype. It automates the end-to-end audit lifecycle, translating raw technical findings (e.g., vulnerability scans) into quantified risk scores and cross-referenced compliance reports.

The primary goal is to address **audit fatigue** by providing a single, automated source of truth for risk and compliance posture across multiple regulatory frameworks.

---

## System Architecture & Technology Stack

The project adheres to microservice design principles, ensuring modularity and maintainability.

### I. Architectural Layers

| Layer | Function | Key Components |
| :--- | :--- | :--- |
| **Ingestion** | Validation, Normalization, Data Persistence | FastAPI, Pydantic, Pandas |
| **Core Logic** | Dynamic Risk Assessment (L x I), Cross-Framework Mapping | SQLAlchemy ORM, PostgreSQL, Python Logic |
| **Analytics** | Aggregation, Reporting Data Generation | SQL Aggregations (`GROUP BY`, `COUNT`), Jinja2 |
| **Presentation** | Interactive Dashboard (Risk Trend, Maturity View) | React/Next.js, Tailwind CSS |

### II. Core GRC Logic Highlight

* **Risk Engine:** Implements the classic security model: $\text{Risk Score} = \text{Likelihood} \times \text{Impact}$. The calculation uses **Normalized Severity** (Likelihood) and **CIA Triad analysis** (Impact) to provide a measurable, business-relevant score.
* **Compliance Mapper:** A many-to-many persistence model that automatically maps a single technical finding to all relevant controls within multiple standards, including **NIST SP 800-53** and **ISO 27001**, eliminating manual cross-walk auditing.

---

## Setup and Deployment

### Prerequisites

* **Docker Desktop** (Required for containerization of API and Database)
* **Node.js / npm** (Required for the Next.js frontend)

### Quick Start (Full Stack)

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/gnanadeepakny/GRC-MMAP.git](https://github.com/gnanadeepakny/GRC-MMAP.git)
    cd GRC-MMAP
    ```

2.  **Start Backend Services (API & DB):** This command builds images, runs the database, and executes the initial seeding logic (CORS and Healthcheck are pre-configured).
    ```bash
    docker-compose up --build
    ```

3.  **Start Frontend (UI):** Open a **second terminal**.
    ```bash
    cd ui
    npm install
    npm run dev
    ```

### Access Points

| Service | URL | Purpose |
| :--- | :--- | :--- |
| **Dashboard** (Frontend) | `http://localhost:3000` | Primary application view (Risk Trend, Maturity). |
| **API Docs** (Swagger) | `http://localhost:8000/docs` | Backend API documentation and testing interface. |
| **Executive Report** | `http://localhost:8000/reports/generate/executive` | One-click HTML summary (Data must be ingested first). |

---

## Usage and Data Ingestion

The system requires initial data ingestion via the Swagger UI after startup.

1.  Navigate to the API Docs: `http://localhost:8000/docs`
2.  Use the **POST /findings/upload\_csv/{source\_name}** endpoint.
3.  Upload the **`data/demo_scan_critical.csv`** file to populate the database with findings, risks, and compliance links.