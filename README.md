# Blog App

A production-ready **Next.js Blog Application** with a fully automated **CI/CD pipeline** using **GitHub, Jenkins, Docker, Docker Hub, AWS EC2, and CloudFormation**.

Whenever code is pushed to the `main` branch, Jenkins automatically:

1. Creates or updates the AWS infrastructure.
2. Builds the Docker image.
3. Pushes the image to Docker Hub.
4. Deploys the latest container to an EC2 instance.

---

# Tech Stack

- Next.js
- Docker
- Jenkins
- Docker Hub
- AWS EC2
- AWS CloudFormation
- GitHub Webhooks

---

# Project Structure

```
blog-app/
│
├── app/
├── public/
├── Dockerfile
├── package.json
├── next.config.ts
├── cloudformation/
│   └── ec2.yaml
│
├── generated/
│   └── blog_app/
│       └── Jenkinsfile
│
├── jenkins/
│   ├── jobs/pipelineJob.groovy.template
│   └── seeds/Jenkinsfile
│
├── scripts/
│   └── onboard.py
│
├── templates/
│   ├── Jenkinsfile.template
│
├── projects/
│   └── blog-app.yml
│
└── README.md
```

---

# CI/CD Workflow

```
Developer
     │
     ▼
Git Push
     │
     ▼
GitHub Webhook
     │
     ▼
Jenkins
     │
     ▼
CloudFormation
(Create / Update EC2)
     │
     ▼
Build Docker Image
     │
     ▼
Push Docker Hub
     │
     ▼
SSH to EC2
     │
     ▼
Pull Latest Docker Image
     │
     ▼
Run Container
```

---

# Features

- Automated Infrastructure Creation
- Infrastructure as Code (CloudFormation)
- Dockerized Next.js Application
- Automatic Docker Image Build
- Docker Hub Integration
- Automated Deployment
- GitHub Webhook Trigger
- Jenkins Pipeline
- Zero Manual Deployment

---

# Prerequisites

Install:

- Git
- Docker
- Jenkins
- AWS CLI
- Python 3
- Job DSL Plugin
- Pipeline Plugin
- AWS Steps Plugin
- SSH Agent Plugin

---

# Jenkins Credentials

Create the following credentials.

| ID | Type | Purpose |
|----|------|----------|
| github-token | Username + PAT | GitHub Repository |
| dockerhub | Username + Password | Docker Hub |
| aws-creds | AWS Credentials | AWS Access |
| ec2-key | SSH Private Key | EC2 Login |

---

# Configure AWS

Create:

- IAM User
- Access Key
- EC2 Key Pair

Required permissions:

- CloudFormation
- EC2
- Elastic IP
- IAM (if required)

---

# CloudFormation

Infrastructure is created using

```
cloudformation/ec2.yaml
```

Resources created:

- Security Group
- EC2 Instance
- Elastic IP (Optional)
- Elastic IP Association

---

# Configure Project

Edit

```
projects/blog-app.yml
```

Example

```yaml
project:
  name: blog_app
  folder: Blogs

github:
  repo: https://github.com/<username>/blog-app.git
  branch: main

docker:
  image: <dockerhub-user>/blog-app

aws:
  region: ap-south-1
  stackName: blog-app-stack
  instanceType: t3.micro
  keyName: jenkins-key

jenkins:
  credentialsId: github-token
```

---

# Generate Jenkins Configuration

Run

```bash
python3 scripts/onboard.py projects/blog-app.yml
```

Generated files:

```
generated/blog_app/Jenkinsfile

jenkins/jobs/blog_app.groovy
```

---

# Create Jenkins Job

Run the Seed Job.

The Seed Job loads:

```
jenkins/jobs/blog_app.groovy
```

and automatically creates

```
Blogs/
    └── blog_app
```

inside Jenkins.

---

# GitHub Webhook

Add a webhook in GitHub.

```
http://<JENKINS-IP>:8080/github-webhook/
```

Content Type

```
application/json
```

Events

```
Just the push event
```

---

# Deployment Pipeline

The pipeline performs:

### 1. Checkout Repository

Downloads the latest source code.

---

### 2. Create / Update EC2

Deploys CloudFormation.

---

### 3. Wait for EC2

Waits for the instance to become available.

---

### 4. Get Elastic IP

Retrieves the public IP from CloudFormation outputs.

---

### 5. Verify Application

Checks that the Dockerfile exists.

---

### 6. Build Docker Image

```
docker build
```

---

### 7. Push Docker Image

```
docker push
```

---

### 8. Install Docker

If Docker is not installed, Jenkins installs it automatically.

---

### 9. Deploy

```
docker pull

docker stop

docker rm

docker run
```

---

# Access Application

```
http://<Elastic-IP>:3000
```

---

# Useful Commands

Generate Jenkins configuration

```bash
python3 scripts/onboard.py projects/blog-app.yml
```

Run Seed Job

```
Generate-Jobs
```

Build Pipeline

```
Blogs → blog_app
```

---

# Troubleshooting

## Dockerfile not found

Verify that the repository contains:

```
Dockerfile
```

---

## EC2 Creation Failed

Check CloudFormation events.

```
AWS Console

CloudFormation

Events
```

---

## Elastic IP Error

If you receive:

```
AddressLimitExceeded
```

Release unused Elastic IPs or request a quota increase.

---

## Docker Login Failed

Verify the Jenkins credential:

```
dockerhub
```

---

## SSH Failed

Verify:

- EC2 is running
- Security Group allows port 22
- Correct SSH key is configured
- Jenkins has the `ec2-key` credential

---

# Future Improvements

- HTTPS with Nginx
- SSL using Let's Encrypt
- Route53
- Auto Scaling
- Application Load Balancer
- Multi-Environment Deployments
- Blue-Green Deployment
- ECS Deployment
- ECR Integration
- Monitoring with CloudWatch
- Slack Notifications

---

# Author

Akash Negi

---

# License

MIT License