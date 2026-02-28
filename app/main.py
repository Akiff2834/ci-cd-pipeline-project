from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zero-Downtime CI/CD Pipeline Demo",
    description="Akif's production-grade CI/CD pipeline showcase",
    version=os.getenv("APP_VERSION", "1.0.0"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()


@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Akif's Zero-Downtime CI/CD Pipeline is LIVE! 🚀",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "production"),
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint — used by load balancer during Blue/Green deployment.
    Returns 200 only when app is fully ready.
    """
    uptime = time.time() - START_TIME
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "version": os.getenv("APP_VERSION", "1.0.0"),
    }


@app.get("/ready")
def readiness_check():
    """
    Readiness probe — Kubernetes / ALB checks this before sending traffic.
    """
    # Add any DB connection checks etc. here in a real app
    return {"status": "ready"}


@app.get("/info")
def get_info():
    return {
        "project": "Zero-Downtime CI/CD Pipeline",
        "author": "Akif",
        "stack": ["Python", "FastAPI", "Docker", "Terraform", "GitHub Actions", "AWS"],
        "deployment_strategy": "Blue/Green",
        "pipeline_stages": ["Lint", "Test", "Build", "Push to ECR", "Deploy to EC2"],
    }
