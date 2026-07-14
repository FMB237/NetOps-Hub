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
| 2    | Configure FastAPI               | ⏳      |
| 3    | Configure PostgreSQL            | ⏳      |
| 4    | Configure SQLAlchemy            | ⏳      |
| 5    | Create Device Model             | ⏳      |
| 6    | Create Pydantic Schemas         | ⏳      |
| 7    | Configure Database Session      | ⏳      |
| 8    | Create API Router               | ⏳      |



**Sprint 2 : DataBase Model**
Let fill our enums.py Where we gonna defined our network architectecture 
1. For that we gonna move to the models folder and creater a simple python file call emuns.py
2. Now let create the device.py where we gonna keep all the infos about the devices in our project so we gonna used the command cd app/models && touch device.py
**This is the distributed Attributes table for the db**

| Field            | Type                     | Required       |
| ---------------- | ------------------------ | -------------- |
| id               | UUID                     | ✅              |
| hostname         | String                   | ✅              |
| ip_address       | String                   | ✅              |
| vendor           | Enum                     | ✅              |
| model            | String                   | ✅              |
| device_type      | Enum                     | ✅              |
| operating_system | String                   | ✅              |
| ssh_port         | Integer                  | ✅ (default 22) |
| username         | String                   | ❌              |
| password         | String (encrypted later) | ❌              |
| location         | String                   | ❌              |
| notes            | Text                     | ❌              |
| created_at       | Timestamp                | ✅              |
| updated_at       | Timestamp                | ✅              |


3. Now Let move on to step3 of the DB design go back to the models folder  and create a file call __init__.py 
4. move back to the database folder where i forgot to create the base.py,database.py
5. Create  a test_connection.py to test the db first 
6. Move to the main.py file and launch the DB
7. To solve the error path i create  a simple run.sh (script) for running the app using the absolute path 
8. But this is not good if we are in production so we will go back the the NetOps-Hub folder and used the command **uvicorn app.main:app --reload** to run our code.