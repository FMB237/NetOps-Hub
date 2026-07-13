# Used to create the project Stucture of the app

mkdir -p app/{api,core,database,models,routers,schemas,services,static,templates}
mkdir backups docker kubernetes terraform tests
mkdir -p .github/workflows

touch app/main.py
touch README.md
touch Dockerfile
touch docker-compose.yml
touch .gitignore
touch .env.example
touch LICENSE