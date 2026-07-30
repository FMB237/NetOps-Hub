# NetHub-Ops 

**Progres Internship Projects**

What is NetHub-Ops a Proffesional Software for network management build using FastAPI(backend) Postgres as Database and many other tools 

It is been build up by FMB237 for the Progre Internship.
---
This project will mainly to be develop in 7 Sprint :
**Sprint 1**
- Create the FastAPI project
 -Configure PostgreSQL
- Create the database models
- Build the dashboard layout

**Sprint 2**
- Device CRUD (Create, Read, Update, Delete)
- Search and filter devices

**Sptint 3**
- Ping functionality
- SSH connectivity testing

**Sprint 4**
- Configuration backup using Netmiko
- Activty Logging

**Sprint 5**
- Dockerize the Application(Task2)

**Sprint 6**
- Github Action CI/CD pipeline(Task3)

**Sprint 7**
- Kubernetes deployment and Terrafrom(Task4)
---

**Packet Installation and activation**
python3 -m venv .venv (Installation)
Source .venv/bin/activate (Activation)

**Portgres Set up using Docker in Local**
For  this project since i have Some portgres containers in my machine i will simply set up a simple  external db so that will not have problems in deployment.



| Step | Goal                            | Status |
| ---- | ------------------------------- | ------ |
| 1    | Design the project architecture | 🟢     |
| 2    | Configure FastAPI               | 🟢     |
| 3    | Configure PostgreSQL            | 🟢     |
| 4    | Configure SQLAlchemy            | 🟢     |
| 5    | Create Device Model             | 🟢     |
| 6    | Create Pydantic Schemas         | 🟢     |
| 7    | Configure Database Session      | 🟢     |
| 8    | Create API Router               | 🟢     |
| 9    | Device CRUD Operations          | 🟢     |
| 10   | Search and Filter Devices       | 🟢     |
| 11   | Ping Functionality              | 🟢     |
| 12   | SSH Connectivity Testing        | 🟢     |
| 13   | Configuration Backup (Netmiko)  | 🟢     |
| 14   | Activity Logging                | 🟢     |
| 15   | Dockerize Application           | 🟢     |
| 16   | GitHub Actions CI/CD            | ⏳      |
| 17   | Kubernetes Deployment           | ⚪      |
| 18   | Terraform Integration           | ⚪      |



**Since we are now at Sprint 6 let try and do it steps by steps**
Let Create our github action directory and start building our yaml file 
Using the command mkdir -p .github/workflows && touch .github/workflows/ci-cd.yml For creating the files for viewing what we have do to mainly 
Let start our main CI-CD Configurations 
