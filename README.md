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
## By Hamza: EKS Deployment & Configuration

1. AWS Authentication
Import AWS Academy credentials into your terminal if you havent done so yet

- export AWS_ACCESS_KEY_ID=your_access_key
- export AWS_SECRET_ACCESS_KEY=your_secret_key
- export AWS_SESSION_TOKEN=your_session_token

2. Create the EKS Cluster
Use the project’s configuration file to create the EKS cluster:

# eksctl create cluster -f k8s/eks-config.yaml

3. Setup Namespace
Create the required namespace:

kubectl create namespace final

4. S3 Background Image Setup
Download a background image and upload it to your private S3 bucket:

# 1. Download a background image
wget https://images.unsplash.com/photo-1579546929518-9e396f3cc809 -O background.jpg

# 2. Upload the image to your bucket
aws s3 cp background.jpg s3://hamza-project/background.jpg

5. Update Manifest Configurations
ConfigMap: Update k8s/config.yaml to use the live S3 bucket URL (BG_IMAGE_URL).
Flask Deployment: Update k8s/flask-deployment.yaml to use your ECR image URI:
975050319979.dkr.ecr.us-east-1.amazonaws.com/clo835-final-project:latest

6. Create Service Account
kubectl create serviceaccount clo835 -n final

7. Deploy & Verify
kubectl apply -f k8s/

# Wait 60 seconds for pods to start
kubectl get pods -n final

8 Change backround image
Upload any image you like to the S3 bucket

change the url in k8s/01-configmap.yaml

# apply commands and refresh page 
kubectl apply -f k8s/01-configmap.yaml
kubectl rollout restart deployment/flask-app -n final


