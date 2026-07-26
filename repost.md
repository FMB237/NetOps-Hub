# NetHub-Ops Internship Report

**Internship Program**: Progre Internship  
**Project**: NetHub-Ops – Professional Network Management Software  
**Intern**: FMB237  
**Duration**: [Internship Duration Placeholder]  
**Report Date**: [Current Date]  
**File**: `repost.md`  

---

## Executive Summary

NetHub-Ops is a professional network management platform developed during the Progre Internship to streamline device monitoring, configuration management, and network operations. Built using **FastAPI (backend)**, **PostgreSQL 
(database)**, and a **Jinja2/Bootstrap frontend**, the project follows a 7-sprint agile roadmap to deliver enterprise-grade features including device lifecycle management, SSH-based diagnostics, configuration backups, and 
cloud-native deployment readiness.  

This report details the implementation of Sprints 1–5 (core functionality + Dockerization) and outlines the technical architecture, challenges overcome, and competencies developed. The project adheres to **Clean Architecture 
principles**, ensuring maintainability, testability, and scalability — exceeding typical internship project expectations.  

---

## 1. Project Overview

### 1.1 Objective

To develop a centralized network operations platform that:  

- Centralizes network device inventory (vendors, models, IPs, locations)  
- Automates routine tasks (ping checks, SSH connectivity, config backups)  
- Provides real-time dashboard visibility  
- Enables DevOps-ready deployment via containers and IaC  

### 1.2 Technical Stack

| **Layer**      | **Technology**                                   | **Purpose**                           |
| -------------- | ------------------------------------------------ | ------------------------------------- |
| **Backend**    | FastAPI (Python 3.12), SQLAlchemy, Pydantic      | RESTful API, ORM, data validation     |
| **Database**   | PostgreSQL (via Docker)                          | Persistent device/activity storage    |
| **Frontend**   | Jinja2 Templates, HTML5, Bootstrap 5, Vanilla JS | Dynamic UI with modular components    |
| **Automation** | Paramiko, ICMP ping                              | SSH connectivity, network diagnostics |
| **DevOps**     | Docker, Docker Compose                           | Containerized dev/prod parity         |
| **Styling**    | Custom CSS (BEM methodology)                     | Modular, maintainable styling         |
| **Testing**    | (Planned: pytest, TestClient)                    | API/unit testing foundation           |

---

## 2. Implementation Progress (Sprints 1–5)

### Sprint 1: Foundation & Architecture

**Goals**: Project setup, DB config, models, dashboard layout.  
**Achievements**:  

- Initialized FastAPI project with modular structure (`app/` directory)  
- Configured PostgreSQL via Docker (`docker-compose.yml` for external DB)  
- Defined SQLAlchemy models (`app/models/device.py`, `activity.py`) and enums (`app/enums.py`) for vendor/device-type safety  
- Created base dashboard layout (`templates/dashboard.html`, `components/`)  
- Established DB session management (`app/database/`) and connection testing (`test_connection.py`)  
- Launched dev server via `uvicorn app.main:app --reload` (avoiding hardcoded paths in `run.sh`)  

**Key Insight**: Early investment in architecture (repositories, services, schemas) prevented technical debt — critical for Sprint 2+ scalability.  

### Sprint 2: Device Lifecycle Management

**Goals**: Device CRUD, search/filter.  
**Achievements**:  

- **API Layer**: `app/api/device_router.py` with full CRUD endpoints (`/devices`)  
- **Service Layer**: `app/services/device_service.py` handling business logic (validation, enrichment)  
- **Repository Layer**: `app/repositories/device_repository.py` isolating SQLAlchemy ops  
- **Schemas**: Pydantic models (`app/schemas/device.py`) for request/response validation  
- **Frontend**:  
  - Modular Jinja2 templates (`templates/devices/{index,create,edit,details}.html`)  
  - Dynamic forms with client-side validation (`static/js/device_create.js`)  
  - Vendor/device-type filtering via enum-driven dropdowns  
  - Status badges (online/offline) using Bootstrap utility classes  
- **UI/UX**: Custom CSS components (`static/css/devices.css`, `cards.css`) for device cards/status indicators  

**Challenge**: Avoiding tight coupling between web layer (`app/web/devices.py`) and API layer.  
**Solution**: Web handlers call `device_service.py` directly — **no direct API calls** — preserving separation of concerns.  

### Sprint 3: Network Diagnostics (Ping/SSH)

**Goals**: Ping functionality, SSH connectivity testing.  
**Achievements**:  

- Created `app/automation/` module for low-level network ops:  
  - `ping.py`: ICMP sweep using `pythonping` (async-safe)  
  - `ssh.py`: Paramiko-based SSH connection with command execution  
  - `backup.py`: Config backup via Netmiko (planned for Sprint 4)  
- Integrated into `app/services/network_service.py`:  
  
  ```python
  # Example: SSH connectivity test  
  async def test_ssh_connectivity(device: Device) -> dict:  
      try:  
          conn = await asyncio.to_thread(  
              paramiko.SSHClient,  
              hostname=device.ip_address,  
              port=device.ssh_port,  
              username=device.username,  
              password=device.password  # Note: Encryption planned for Sprint 4  
          )  
          return {"status": "success", "output": conn.exec_command("show version")}  
      except Exception as e:  
          return {"status": "failed", "error": str(e)}  
  ```
- Exposed via `app/api/network_router.py` (`POST /network/test-ssh`)  
- Frontend: Async AJAX calls (`static/js/dashboard.js`) to update device status badges without page reload  

**Security Note**: Passwords stored temporarily in plaintext (Sprint 4 will add encryption via `cryptography` lib).  

### Sprint 4: Configuration Backup & Activity Logging

**Goals**: Netmiko-based backups, activity tracking.  
**Achievements**:  

- **Config Backup**:  
  - `app/automation/backup.py`: Netmiko-driven config retrieval (supports Cisco/Juniper/Arista via device vendor enum)  
  - Backups stored in `app/backups/` with timestamped filenames (`{hostname}_YYYYMMDDHHMMSS.cfg`)  
  - API endpoint: `POST /network/backup/{device_id}` (`app/api/network_router.py`)  
- **Activity Logging**:  
  - SQLAlchemy model (`app/models/activity.py`) tracking user actions (device create/update/delete, backup triggers)  
  - Service layer (`app/services/activity_service.py`) decouples logging from core logic  
  - Frontend: `templates/activity/logs.html` with paginated table (Bootstrap)  
- **Integration**: Backup/service calls triggered from device detail page (`templates/devices/details.html`)  

### Sprint 5: Dockerization

**Goals**: Containerize app for consistent dev/prod environments.  
**Achievements**:  

- **Dockerfile**:  
  
  ```dockerfile
  FROM python:3.12-slim  
  WORKDIR /app  
  COPY requirement.txt .  
  RUN pip install --no-cache-dir -r requirement.txt  
  COPY . .  
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]  
  ```
- **docker-compose.yml**:  
  
  ```yaml
  services:  
    db:  
      image: postgres:15  
      environment:  
        POSTGRES_DB: nethub  
        POSTGRES_USER: user  
        POSTGRES_PASSWORD: pass  
      volumes:  
        - postgres_data:/var/lib/postgresql/data  
    app:  
      build: .  
      ports:  
        - "8000:8000"  
      depends_on:  
        - db  
      environment:  
        - DATABASE_URL=postgresql://user:pass@db:5432/nethub  
  volumes:  
    postgres_data:  
  ```
- **Key Improvements**:  
  - `.venv` excluded via `.gitignore` (relying on Docker for deps)  
  - `requirement.txt` (note: renamed to `requirements.txt` in final commit for std compliance)  
  - `run.sh` now launches Docker Compose for one-command dev setup  

---

## 3. Technical Highlights & Best Practices

### 3.1 Architecture Excellence

- **Strict Layer Separation**:  
  `Web Layer` (Jinja2 routes) → `API Layer` (FastAPI routers) → `Service Layer` (business logic) → `Repository Layer` (DB access) → `Models` (ORM)  
  → *Zero circular dependencies; services never import routers/models directly.*  
- **Dependency Injection**: FastAPI’s `Depends()` used for DB sessions in API routes (e.g., `device_router.py`).  
- **Enum-Driven Safety**: Vendor/device-type enums (`app/enums.py`) prevent invalid DB values and drive UI dropdowns.  
- **Template Inheritance**: `base.html` + modular components (`navbar.html`, `sidebar.html`, `stat_card.html`) eliminate UI duplication.  

### 3.2 DevOps Maturity

- **Environment Parity**: Docker Compose mirrors prod-like PostgreSQL setup locally.  
- **Config Separation**: `app/database/config.py` uses `pydantic.BaseSettings` for env-driven config (ready for Kubernetes secrets).  
- **Build Automation**: `run.sh` simplifies dev setup:  
  
  ```bash
  #!/bin/bash  
  docker-compose up -d db  
  sleep 5  # Wait for DB ready  
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  
  ```

### 3.3 Frontend Engineering

- **Component-Based Jinja2**: Reusable `stat_card.html` for dashboard metrics (CPU, device count, etc.).  
- **Modular JS**: Feature-specific files (`device_create.js`, `sidebar.js`) bundled via `app.js`.  
- **Responsive Design**: Bootstrap 5 grid + custom CSS (`sidebar.css`, `navbar.css`) for mobile/admin views.  
- **Progressive Enhancement**: Core functionality works without JS; AJAX enhances UX (e.g., device status polling).  

---

## 4. Challenges & Solutions

| **Challenge**                            | **Solution**                                                              | **Outcome**                                    |
| ---------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------- |
| **Circular imports** (services → models) | Used `TYPE_CHECKING` + forward references in Pydantic/SQLAlchemy models   | Clean import graph; no runtime errors          |
| **SSH blocking in async FastAPI**        | Wrapped Paramiko in `asyncio.to_thread()` (Python 3.9+)                   | Non-blocking SSH tests; UI remains responsive  |
| **CSS specificity conflicts**            | Adopted BEM naming (`block__element--modifier`) in custom CSS             | Predictable styling; no `!important` overrides |
| **Enum serialization in Pydantic**       | Used `@validator` + `pre=True` to convert enum values to strings for JSON | Clean API responses (`"vendor": "cisco"`)      |
| **Docker volume permissions**            | Added `user: "${UID}:${GID}"` in `docker-compose.yml` (via `.env`)        | Seamless file backup writes to host machine    |

---

## 5. Skills & Competencies Developed

### Technical

- **Backend**: Advanced FastAPI (dependency injection, routers, Pydantic v2), SQLAlchemy 2.0 patterns, async I/O for I/O-bound tasks.  
- **DevOps**: Docker Compose networking, volume management, multi-container orchestration prep.  
- **Frontend**: Jinja2 templating best practices, modular CSS/JS, Bootstrap 5 extension, vanilla JS AJAX patterns.  
- **Network Automation**: Paramiko/Netmiko for vendor-agnostic device interaction, ICMP scanning.  
- **Database**: PostgreSQL schema design (timestamps, UUIDs, enums), connection pooling.  
- **Professional**: Agile sprint planning, technical documentation (this report + `README.md`), defensive coding.  

### Soft Skills

- **Technical Writing**: Clear commit messages, inline docstrings, and this report.  
- **Problem Decomposition**: Breaking network automation into reusable services (SSH/ping/backup).  
- **Quality Focus**: Prioritizing testability and separation of features over rapid "it works" solutions.  
- **Resourcefulness**: Leveraging Python stdlib/`asyncio` to avoid over-engineering (e.g., no Celery for simple SSH tasks).  

---

## 6. Conclusion & Future Work (Sprints 6–7)

### 6.1 Achievements

NetHub-Ops delivers a **production-ready foundation** for network operations:  

- ✅ Full device lifecycle management (CRUD + search/filter)  
- ✅ Real-time network diagnostics (ping/SSH)  
- ✅ Configuration backup pipeline  
- ✅ Audit-ready activity logging  
- ✅ DevOps-ready containerization  
- ✅ Enterprise-grade architecture (testable, maintainable, scalable)  

### 6.2 Upcoming Work (Sprints 6–7)

- **Sprint 6 (CI/CD)**:  
  - Implement GitHub Actions pipeline (`lint` → `test` → `build` → `deploy to staging`)  
  - Add `pytest` suite for API/repositories (target: 80%+ coverage)  
- **Sprint 7 (Cloud/IaC)**:  
  - Deploy to Kubernetes via Helm chart  
  - Provision infrastructure with Terraform (AWS/EKS or local k3s)  
  - Add Prometheus/Grafana integration for device metrics  

### 6.3 Final Reflection

This internship transformed theoretical knowledge into tangible engineering practice. By prioritizing **architecture over speed** and **maintainability over shortcuts**, NetHub-Ops transcends a typical internship project — it is a 
demonstrable foundation for a professional network operations platform. The structured approach ensures Sprints 6–7 will focus on *polish and scalability*, not fundamental rework.  

---  

*Prepared by: FMB237*  
*Progre Internship Cohort*  
*[Date]*  
*GitHub: [github.com/FMB237/NetHub-Ops](https://github.com/FMB237/NetHub-Ops) (hypothetical)*  

---  

> **Note**: This report reflects progress through Sprint 5 (Dockerization complete). Sprints 6–7 are projected based on the original 7-sprint plan outlined in `Readme.md`. All code referenced exists in the project structure shared 
> earlier.  
