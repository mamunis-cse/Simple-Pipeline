# 🧱 Complete CI/CD Pipeline for Flask App using GitHub Actions, Docker Hub, and SSH Deployment

This page contains **everything step by step** to set up CI/CD for a Python (Flask) application, including GitHub Actions workflow, Docker configuration, Docker Hub setup, SSH deployment, and server script.

---

## 📂 Project Structure

```
Simple-Pipeline/
├── app.py                  # Your Flask application code
├── requirements.txt        # Python dependencies
├── Dockerfile              # Instructions to build Docker image
└── .github/
    └── workflows/
        └── docker-deploy.yml  # GitHub Actions workflow for CI/CD
├── deploy.sh               # Script to deploy Docker image on server
```

---

## 1️⃣ GitHub Repository Setup

✅ Your Python app (e.g., Flask) is hosted on GitHub.
✅ A Dockerfile is present in the root directory of the project.
✅ GitHub Actions workflow file is located at: `.github/workflows/docker-deploy.yml`

---

## 2️⃣ Quick Explanation of Each File

| File                                  | Purpose                                                                                |
| ------------------------------------- | -------------------------------------------------------------------------------------- |
| `app.py`                              | Main Flask application file.                                                           |
| `requirements.txt`                    | List of Python packages needed to run your app.                                        |
| `Dockerfile`                          | Defines how to containerize your app (base image, dependencies, run command).          |
| `.github/workflows/docker-deploy.yml` | GitHub Actions workflow: builds Docker image, pushes to Docker Hub, deploys via SSH.   |
| `deploy.sh`                           | Script that runs on the server to pull the new Docker image and restart the container. |

---

## 3️⃣ GitHub Actions Workflow (`docker-deploy.yml`)

```yaml
name: Build and Push Docker Image  ##### Name of the workflow shown in GitHub Actions UI

on:
  push:
    branches: [ main ]  ##### Trigger this workflow only when code is pushed to the 'main' branch

jobs:
  build-and-push:  ##### First job: Build and push Docker image to Docker Hub
    runs-on: ubuntu-latest  ##### Use the latest Ubuntu runner provided by GitHub

    steps:
      - name: Checkout code
        uses: actions/checkout@v3  ##### Step 1: Pull the latest code from the repository

      - name: Log in to Docker Hub
        uses: docker/login-action@v2  ##### Step 2: Log in to Docker Hub using credentials
        with:
          username: ${{ secrets.DOCKER_USERNAME }}  ##### Docker Hub username stored in GitHub Secrets
          password: ${{ secrets.DOCKER_PASSWORD }}  ##### Docker Hub password/token stored in GitHub Secrets

      - name: Build Docker image
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/flask-ci-cd-app:latest .  ##### Build Docker image with 'latest' tag
          docker tag ${{ secrets.DOCKER_USERNAME }}/flask-ci-cd-app:latest ${{ secrets.DOCKER_USERNAME }}/flask-ci-cd-app:${{ github.sha }}  ##### Tag image with commit SHA for versioning

      - name: Push Docker image
        run: |
          docker push ${{ secrets.DOCKER_USERNAME }}/flask-ci-cd-app:latest  ##### Push 'latest' tag to Docker Hub
          docker push ${{ secrets.DOCKER_USERNAME }}/flask-ci-cd-app:${{ github.sha }}  ##### Push SHA-tagged version to Docker Hub

  deploy:  ##### Second job: Deploy the Docker image to your server
    runs-on: ubuntu-latest
    needs: build-and-push  ##### This job runs only after 'build-and-push' completes successfully

    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1.1.0  ##### Use SSH to connect to your server
        with:
          host: ${{ secrets.SERVER_HOST }}  ##### Server IP or domain stored in GitHub Secrets
          username: ${{ secrets.SERVER_USERNAME }}  ##### SSH username (e.g., root)
          key: ${{ secrets.SERVER_SSH_KEY }}  ##### SSH private key stored in GitHub Secrets
          script: |
            bash /root/ci_cd/deploy.sh ${{ github.sha }}  ##### Run the deploy script on the server with the image tag (SHA)

```

---

## 4️⃣ Docker Hub Setup

1. Click on your profile → Repositories → Create Repository.

2. Fill in:

   * **Name**: `flask-ci-cd-app`
   * **Visibility**: Public or Private
   * Leave the rest as default → Click **Create**

3. Generate Docker Hub Access Token (Recommended)

   * Go to [Docker Hub Security](https://hub.docker.com/settings/security) → Access Tokens → New Access Token
   * Name it (e.g., `github-actions-token`)

---

## 5️⃣ GitHub Secrets Configuration

Add the following secrets in **GitHub → Settings → Secrets and Variables → Actions**:

| Secret Name       | Value                               |
| ----------------- | ----------------------------------- |
| `DOCKER_USERNAME` | Your Docker Hub username            |
| `DOCKER_PASSWORD` | Docker Hub Access Token or password |
| `SERVER_HOST`     | Your server IP or domain            |
| `SERVER_USERNAME` | SSH username (e.g., root)           |
| `SERVER_SSH_KEY`  | SSH private key for deployment      |

---

## 6️⃣ SSH Setup for GitHub Deployment

✅ Step-by-step summary:

✔️ Log into your server using SSH:

```bash
ssh user@server_ip
```

✔️ Generate SSH key pair:

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions"
```

✔️ Add the **public key** to `~/.ssh/authorized_keys` on the server.
✔️ Copy the **private key** and add it to GitHub Secrets as `SERVER_SSH_KEY`.

---

## 7️⃣ Deploy Script (`deploy.sh`)

```bash
#!/bin/bash

##### === Basic Configuration ===
APP_NAME="flask-ci-cd-app"
DOCKER_USER="mamunredhat"
IMAGE_TAG=${1:-latest}
PORT=5000

echo "Deploying $APP_NAME:$IMAGE_TAG"

##### === Pull the Docker image from Docker Hub ===
docker pull $DOCKER_USER/$APP_NAME:$IMAGE_TAG || exit 1

##### === Stop old container if running ===
docker stop $APP_NAME 2>/dev/null || true

##### === Remove old container if exists ===
docker rm $APP_NAME 2>/dev/null || true

##### === Run new container ===
docker run -d --name $APP_NAME -p $PORT:5000 $DOCKER_USER/$APP_NAME:$IMAGE_TAG || exit 1

echo "Deployment successful"
```

---

✅ **Pipeline Ready:** Push code to `main` → GitHub Actions builds Docker image → pushes to Docker Hub → SSH deploys automatically.
