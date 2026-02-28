# 🚀 Zero-Downtime CI/CD Cloud Pipeline

[![CI/CD Pipeline](https://github.com/akif/ci-cd-pipeline-project/actions/workflows/deploy.yml/badge.svg)](https://github.com/akif/ci-cd-pipeline-project/actions)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![Docker](https://img.shields.io/badge/Docker-multi--stage-blue)
![Terraform](https://img.shields.io/badge/Terraform-AWS-purple)
![Deploy](https://img.shields.io/badge/Deploy-Blue%2FGreen-green)

A **production-grade CI/CD pipeline** built from scratch using GitHub Actions, Docker, Terraform, and AWS.  
Every `git push` to `main` triggers an automated pipeline that tests, builds, and deploys with **zero downtime**.

---

## 🏗️ Architecture

```
Developer → git push → GitHub Actions
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
             🧪 Test    🐳 Build     🟢 Deploy
           (pytest +   (Docker →   (Blue/Green
            flake8)   ECR push)    on EC2)
```

### Pipeline Stages

| Stage | Tool | What it does |
|-------|------|--------------|
| **Lint** | flake8 | Catches syntax errors & style issues |
| **Test** | pytest + coverage | Runs unit tests, fails if coverage < 80% |
| **Build** | Docker (multi-stage) | Builds a lean, non-root production image |
| **Push** | Amazon ECR | Stores versioned image (tagged by git SHA) |
| **Deploy** | SSH + Docker | Blue/Green swap with health-check gating |

---

## 🔵🟢 Zero-Downtime: Blue/Green Deployment

Instead of restarting the live container (which causes downtime), the pipeline:

1. **Starts a GREEN** container on port `8001` (hidden from users)
2. **Health-checks GREEN** — waits up to 60s for `/health` to return 200
3. **Switches traffic** — stops BLUE, restarts GREEN on port `8000`
4. **Auto-rollback** — if health check fails, GREEN is destroyed, BLUE stays live

---

## 🛠️ Tech Stack

- **App**: Python + FastAPI
- **Container**: Docker (multi-stage build, non-root user)
- **Registry**: Amazon ECR (with vulnerability scanning)
- **Infrastructure**: Terraform (VPC, EC2, Security Groups, Elastic IP)
- **Pipeline**: GitHub Actions
- **Deployment**: Blue/Green strategy via SSH

---

## ⚙️ Setup Guide

### 1. Prerequisites
- AWS account (Free Tier works)
- Terraform >= 1.5
- Docker
- GitHub account

### 2. Provision AWS Infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

This creates: VPC, Subnet, Security Group, EC2 (t2.micro), Elastic IP, ECR repo.

### 3. Configure GitHub Secrets

In your repo → Settings → Secrets → Actions, add:

| Secret | Value |
|--------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `EC2_HOST` | Elastic IP from Terraform output |
| `EC2_SSH_KEY` | Contents of your `.pem` private key |

### 4. Deploy!

```bash
git add .
git commit -m "feat: initial deployment"
git push origin main
```

Watch the pipeline run at: `https://github.com/<you>/ci-cd-pipeline-project/actions` 🎉

---

## 📁 Project Structure

```
ci-cd-pipeline-project/
├── app/
│   └── main.py                    # FastAPI application
├── tests/
│   └── test_main.py               # pytest unit tests
├── terraform/
│   ├── main.tf                    # AWS infrastructure (VPC, EC2, ECR)
│   ├── variables.tf               # Configurable variables
│   └── outputs.tf                 # IP, ECR URL outputs
├── scripts/
│   └── manual-deploy.sh           # Optional manual deploy helper
├── .github/
│   └── workflows/
│       └── deploy.yml             # Full CI/CD pipeline definition
├── Dockerfile                     # Multi-stage, non-root build
├── requirements.txt
└── README.md
```

---

## 🔗 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | App info & version |
| `GET /health` | Health check (used by pipeline) |
| `GET /ready` | Readiness probe |
| `GET /info` | Stack & deployment details |

---

*Built to demonstrate real-world DevOps skills: IaC, containerization, automated testing, and zero-downtime deployments.*
