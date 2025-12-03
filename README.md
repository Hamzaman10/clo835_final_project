By Keyan:

To test locally:
  
fill in the .env var
  
  
docker build -t sample-app .
  
docker network create clo-network
  
docker run --name mysql-db --network clo-network \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=employees \
  -p 3306:3306 \
  mysql:5.7
  
docker run -p 8080:81 --network clo-network sample-app --env-file .env

------------------------------------------------------------------------------------------------------------------------------------------------------

By Wes:

# CLO835 Final Project - Application & CI/CD

This repository contains the source code for the **CLO835 Final Project (Task 1 & 3)**. It includes the enhanced Flask application and a GitHub Actions workflow that automatically builds, tests, and publishes the Docker image to Amazon ECR.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/weswangw/clo835_final_project.git
cd clo835_final_project
```

---

## 2. Security & Environment Variables

**IMPORTANT:** The `.env` file containing secrets is not included in this repository for security reasons.  
You **must** create it locally to run the application.

Create a new file named `.env` in the root directory and populate it with:

```bash
# Database Configuration (for local testing)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB=employees
MYSQL_PORT=3306

# App Configuration
HEADER_NAME=YourName
BG_IMAGE_URL=s3://your-bucket/image.jpg

# AWS Credentials (Required for S3 access)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token
AWS_DEFAULT_REGION=us-east-1
```

---

## 3. Running Locally (Docker)

To test the application on your local machine with the database:

```bash
# 1. Build the image
docker build -t sample-app .

# 2. Create the network
docker network create clo-network

# 3. Run the MySQL container
docker run --name mysql-db --network clo-network   -e MYSQL_ROOT_PASSWORD=password   -e MYSQL_DATABASE=employees   -p 3306:3306   -d mysql:5.7

# 4. Run the Flask App (using your local .env file)
docker run -p 8080:81 --network clo-network --env-file .env sample-app
```

Access the app at: **http://localhost:8080**

---

## CI/CD Pipeline (GitHub Actions)

The repository includes a workflow at:

```
.github/workflows/deploy.yml
```

This workflow triggers on every push to `master`.

### What the pipeline does:
- Builds the Docker image  
- Runs unit tests (DB connection is mocked)  
- Pushes the Docker image to Amazon ECR  

---

## Updating AWS Secrets (For AWS Academy Users)

AWS Academy session tokens expire frequently.  
You **must update GitHub Secrets** before pushing code.

Navigate to:

**Settings → Secrets and variables → Actions**

Update the following:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` *(critical for sandbox accounts)*

---

## Branch Protection

Direct commits to `master` are **disabled**.

Workflow:
1. Create a new branch  
2. Commit changes  
3. Open a Pull Request (PR) into `master`

---

## Deployment Info (For Task 5)

When creating Kubernetes manifests, reference the image stored in Amazon ECR:

**ECR Repository Name:** `clo835-final-project`

**Image URI Pattern:**
```
975050350494.dkr.ecr.us-east-1.amazonaws.com/clo835-final-project:latest
```

*Note: Replace `975050350494` with your current AWS Academy lab account ID if it changes.*

---
