# NetHub-Ops - Network Operations and Automation Platform

A professional network management system built with FastAPI, PostgreSQL, and modern web technologies. This platform provides device management, network automation, monitoring, and reporting capabilities for network administrators.

## Project Status

| Sprint | Objective | Status |
|--------|-----------|--------|
| **Sprint 1** | Project Foundation | ✅ Completed |
| **Sprint 2** | Device CRUD & Search | ✅ Completed |
| **Sprint 3** | Network Automation | ✅ Completed |
| **Sprint 4** | Configuration Backup & Activity Logging | ✅ Completed |
| **Sprint 5** | Dockerization | ✅ Completed |
| **Sprint 6** | CI/CD Pipeline | ⏳ In Progress |
| **Sprint 7** | Kubernetes & Terraform | ⚪ Not Started |

## ✨ Features Implemented

### Core Functionality
- **Device Management**: Full CRUD operations for network devices
- **Search & Filter**: Find devices by hostname, IP, vendor, or type
- **Network Automation**:
  - Ping testing (ICMP) with latency and packet loss reporting
  - SSH connectivity testing and command execution
  - Configuration backup and restore
  - Support for multiple vendor devices (Cisco, Juniper, Aruba, etc.)
- **Activity Tracking**: Comprehensive audit trail of all user and system actions
- **Responsive Dashboard**: Real-time statistics and visualizations
- **Multi-language Support**: Clean, internationalized interface

### Technical Architecture
- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML/CSS/Bootstrap with Vanilla JavaScript
- **Authentication**: Session-based (extensible)
- **API**: RESTful endpoints with automatic OpenAPI documentation
- **Containerization**: Docker and Docker-Compose ready
- **Monitoring**: Integrated activity logging and system metrics

## 📸 Screenshots

### Dashboard Overview
![Dashboard](project_images/Dashboard.png)

### Device Management
![Device List](project_images/Devices.png)
![Device Details](project_images/Devices_Informations.png)
![Add/Edit Device](project_images/DeviceCreate.png)

### Network Automation
![Ping Testing](project_images/TestingPing.png)
![SSH Testing](project_images/TestingSSH.png)
![Command Execution](project_images/NodeExecution.png)

### Configuration Management
![Backup Interface](project_images/BackupPage.png)
![Backup General View](project_images/BackupGeneral.png)

### Activity Monitoring
![Activity Log](project_images/ActivityLogs.png)

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (ASGI)
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL
- **Network Automation**: Netmiko, Paramiko (fallback), subprocess (ping)
- **Validation**: Pydantic
- **API Documentation**: Swagger UI (via FastAPI)

### Frontend
- **Styling**: Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JS with Fetch API
- **Templating**: Jinja2 (via FastAPI)

### DevOps & Infrastructure
- **Containerization**: Docker & Docker-Compose
- **CI/CD**: GitHub Actions (in progress)
- **Orchestration**: Kubernetes (planned)
- **Infrastructure as Code**: Terraform (planned)

## 📂 Project Structure

```
NetOps-Hub/
├── app/
│   ├── api/                 # API route definitions
│   ├── app/                 # Core application logic
│   ├── automation/          # Network automation modules (Netmiko-based)
│   ├── database/            # Database configuration and models
│   ├── models/              # SQLAlchemy models and Pydantic schemas
│   ├── services/            # Business logic services
│   ├── templates/           # HTML templates (Jinja2)
│   └── web/                 # Web route handlers
├── backups/                 # Configuration backup storage
├── project_images/          # Screenshots for documentation
├── .dockerignore            # Docker build exclusions
├── .env                     # Environment variables
├── .env.example             # Environment template
├── Dockerfile               # Application container definition
├── docker-compose.yml       # Multi-container orchestration
├── requirement.txt          # Python dependencies
├── run.sh                   # Development startup script
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites
- Docker and Docker-Compose (for containerized deployment)
- OR Python 3.8+ and PostgreSQL (for local development)

### Option 1: Docker Deployment (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd NetOps-Hub

# Start the application
docker-compose up -d

# Access the application
# Web UI: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development
```bash
# Clone the repository
git clone <repository-url>
cd NetOps-Hub

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirement.txt

# Set up environment
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
python -c "from app.database.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"

# Run the application
uvicorn app.main:app --reload
```

## 🔧 Configuration

Environment variables are managed through `.env` file:
```env
POSTGRES_USER=netops_admin
POSTGRES_PASSWORD=netops_password
POSTGRES_DB=netops_hub
POSTGRES_HOST=localhost  # Use 'postgres' when running in Docker
POSTGRES_PORT=5434
DATABASE_URL=postgresql://netops_admin:netops_password@localhost:5434/netops_hub

APP_NAME=NetHub-Ops
DEBUG=True
```

## 📚 API Documentation

Once the application is running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

Run the test suite:
```bash
# With Docker
docker-compose exec app pytest

# Local
pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**FMB237** - Developed for the Progressive Internship Program

---

*Last updated: July 27, 2026*