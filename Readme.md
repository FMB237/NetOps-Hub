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
   
**Moving up to Sprint3 Pydantic Schema**
1. Let move on to the folder call schemas and let defined our application main schemas that will fit with models and database structure
2. For that we will created a simple python file call device.py

Now let move on to the repositories that is mainly inside the repository folder to define our project repository.
**Why use a Repository?**

Without a repository:
API
 │
 ▼
SQLAlchemy

With a repository:

This keeps responsibilities separate:

- API → Handles HTTP requests.
 - Service → Business logic.
 - Repository → Database operations.

1. Since we had already created the repository folder then with will just move up to it and create a file call device_repository.py 

**Let Move on and create the services of our app that is mainly our devices various services.**
For that move on to the services folder and create the file device_service.py 


**Building the RESTAPI**
So let move on the to api Folder.Then we gonna create an __init__.py file 
After building our RestAPI let move on and test our API only using the Fastapi docs on the link [text](http://localhost:8000/docs)


Now we are done with the doing of the backend Let move to the Frontend Using (HTML,CSS,Js,BootStrap and Jinja2Templates)
- We need to install Jinja2 then  start Buidling Our Frontend Move on to the static file 
- Now that we have a functional Frontend Prototype let try to make it better 
- By adding devices formats and frontend Router for our HTML Renders
- We are doing this to not mix our API endpoints of the Fastapi with  that of our HTML
- So for that we gonna create a folder inside our project and called it web and inside that folder create a file called views.py that will contain our routers 
- This is the main structure 
- /api/devices → JSON (REST API)
/devices       → HTML (Jinja2)
- After the view.PY configuration register it and include it into the main.py file 
- Then go update the sidebar of our dashboard
- Let update our Web Folder for additional support on our Webviews 
- Instead of a simple an principal views.py for handling the routing let split that into many files
-  **Stucture**
  ├── web/                    # HTML Pages
│   ├── __init__.py
│   ├── dashboard.py
│   ├── devices.py
│   ├── monitoring.py
│   ├── backups.py
│   └── settings.py
With this we have a modular structure instead of a fully centralise app
So let remove the views.py and add  first the dashboard.py file 
We will also create a  and other file that we will used for router for the devices since we did that for the dashboard
So let create a file and call it devices.py that will be store in the path app/web/devices.py
