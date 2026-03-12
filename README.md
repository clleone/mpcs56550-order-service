## Order Service for ECommerce App

This repository houses all code and configuration files related to order
management in my ecommerce application.

### Requirements
- Python 3.11+
- pip
- PostgreSQL 15 (or Docker)
- Git

### Directory Structure
```text
orders/
|   .env
|   .gitignore
|   Dockerfile
|   Jenkinsfile
|   pyproject.toml
|   README.md
|   requirements.txt
|
+---k8s
|   \---order-service
|       +---dev
|       |       configmap.yaml
|       |       deployment.yaml
|       |       service.yaml
|       |
|       +---prod
|       |       configmap.yaml
|       |       deployment.yaml
|       |       service.yaml
|       |
|       \---staging
|               configmap.yaml
|               deployment.yaml
|               service.yaml
|
+---src
|   |   app.py
|   \--- db.py
|
\---tests
    \--- test_orders.py
```
### Instructions to build and run order service locally:
```bash
# Clone the repo
git clone https://github.com/yourusername/mpcs56550-order-service
cd mpcs56550-order-service

# Install dependencies
pip install -r requirements.txt

# Copy environment template and fill in values
cp .env.example .env

# Run the service
python src/app.py
```
Service will be at http://localhost:5002

### Testing:
```bash
# Install test dependencies
pip install pytest pytest-mock

# Run tests
python -m pytest tests/
```

### Docker
```bash
# Build the image
docker build -t order-service .

# Run the container
docker run -p 5002:5002 \
  --env-file .env \
  order-service
```

### GitFlow Overview:
- **Main** - This branch stores the official release history. All commits here are 
tagged with a version number. *Main is a protected branch and requires a pull
request to merge.*
- **Develop** - This branch contains the complete history of the project and serves
as an integration branch for features. *Develop is a protected branch and
requires a pull request to merge.*
- **Feature** - Feature branches are split off of the latest Develop branch to build
new features. Once complete, they are merged back into Develop.
- **Release** - Once a certain amount of features have been completed, a Release
branch is split off Develop. Once this branch is created, no new features are
added, only tidying up existing ones. Once complete, it is merged into Main and
tagged with a version number. It is then also merged into Develop.
- **Hotfix** - These branches exist to quickly patch production releases. They are
the only branches split directly off Main. Once a fix is completed, it is merged
into Main with a new version number and then Develop. (in some cases it might be
merged into a Release branch)

Citation: [Atlassian](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)