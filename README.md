
# LLM-Based Sentiment Analysis Platform

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python)](https://www.python.org/)  
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange?logo=mlflow)](https://mlflow.org/)  
[![Prefect](https://img.shields.io/badge/Prefect-Orchestration-lightgrey?logo=prefect)](https://www.prefect.io/)  
[![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)](https://www.docker.com/)  
[![Jenkins](https://img.shields.io/badge/Jenkins-CI/CD-blue?logo=jenkins)](https://www.jenkins.io/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)  

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features & Contributions](#features--contributions)  
3. [System Architecture](#system-architecture)  
4. [Tech Stack](#tech-stack)  
5. [Setup & Installation](#setup--installation)  
6. [Running the Application](#running-the-application)  
7. [Using the Web App](#using-the-web-app)  
8. [Docker & Jenkins CI/CD](#docker--jenkins-cicd)  
9. [Shared Library Setup](#shared-library-setup)  
10. [Project Structure](#project-structure)  
11. [License](#license)  

---

## Project Overview

This project is a **full-stack LLM-based sentiment analysis platform** for analyzing product reviews.  
It uses **Prefect** for workflow orchestration, **MLflow** for experiment tracking, and **Flask** for the web interface.  

The system supports:

- Ingesting raw product reviews  
- Preprocessing text data  
- Vectorizing using BoW and Word2Vec (CBOW & SkipGram)  
- Training multiple ML models and logging experiments to MLflow  
- Serving predictions via a web UI with retraining capability  
- Fully dockerized deployment with CI/CD pipeline via Jenkins  

---

## Features & Contributions

- End-to-end **ML pipeline** using Prefect & MLflow  
- Modular **data preprocessing** & **vectorization**  
- **Flask web interface** for real-time sentiment prediction  
- **Automatic retraining** from UI input  
- Dockerized environment including MLflow, Prefect, and Flask  
- **CI/CD Pipeline** integrated with Jenkins and DockerHub  
- Shared libraries used for **Jenkins pipeline modularization**  

---

## System Architecture

```

+-----------------+
|   User Input    |
+--------+--------+
|
v
+-----------------+
|   Flask App     |
+--------+--------+
|
v
+-----------------+       +-----------------+
|  Prefect Flow   | ----> |  MLflow Logging |
+--------+--------+       +-----------------+
|
v
+-----------------+
|  ML Models      |
+-----------------+

````

---

## Tech Stack

- **Python 3.10**  
- **Flask** for UI  
- **MLflow** for experiment tracking  
- **Prefect** for orchestration  
- **Scikit-learn** for ML models  
- **Word2Vec & BoW** vectorization  
- **Docker** for containerization  
- **Jenkins** for CI/CD  
- **GitHub Shared Libraries** for Jenkins modularization  

---

## Setup & Installation

### 1. Clone the repositories

**Main project:**
```bash
git clone https://github.com/Harshitraiii2005/LLM-2.git
cd LLM-2
````

**Shared Jenkins library:**

```bash
git clone https://github.com/Harshitraiii2005/jenkins-shared-libraries.git
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Running the Application

### 1. Start MLflow & Prefect Services

```bash
chmod +x start_services.sh
./start_services.sh
```

* MLflow server will run at: `http://localhost:5090`
* Prefect server dashboard: `http://localhost:4200`

### 2. Start Flask App

```bash
python app.py
```

* Open your browser: `http://localhost:9070`
* Enter text to predict sentiment
* Optional: Click **Retrain Pipeline**

---

## Docker Deployment

1. Build Docker Image:

```bash
docker build -t harshitrai20/llm:latest .
```

2. Run Container:

```bash
docker run -p 9070:9070 -p 5090:5090 -p 4200:4200 harshitrai20/llm:latest
```

---

## Jenkins CI/CD Pipeline

**Pipeline Steps:**

1. **Workspace Cleanup** – clean previous builds
2. **Environment Setup** – create virtual environment & install dependencies
3. **Start Services** – run MLflow & Prefect in background
4. **Docker Login** – login using Jenkins credentials (`dockerhub-creds`)
5. **Build Docker Image** – build project image
6. **Push Docker Image** – push to DockerHub

**Jenkinsfile Sample:**

```groovy
@Library('shared') _

pipeline {
    agent any

    environment {
        IMAGE_NAME = "llm"
        DOCKER_USERNAME = "harshitrai20"
    }

    stages {
        stage("Checkout") { steps { checkout scm } }

        stage("Workspace Cleanup") { steps { cleanWs() } }

        stage("Environment Setup") {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage("Start Services") {
            steps {
                sh '''
                    chmod +x start_services.sh
                    ./start_services.sh &
                '''
            }
        }

        stage("Docker Login") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage("Build Docker Image") {
            steps { script { docker_build(env.DOCKER_USERNAME, env.IMAGE_NAME, "latest") } }
        }

        stage("Push Docker Image") {
            steps { script { docker_push(env.DOCKER_USERNAME, env.IMAGE_NAME, "latest") } }
        }
    }

    post {
        success { echo "Image pushed to DockerHub successfully" }
        failure { echo "Pipeline failed, check logs" }
    }
}
```

---

## Shared Library Setup for Jenkins

1. Go to **Manage Jenkins → Configure System → Global Pipeline Libraries**
2. Add new library:

   * Name: `shared`
   * Default Version: `main`
   * Retrieval Method: `Modern SCM` → Git
   * Project Repository: `https://github.com/Harshitraiii2005/jenkins-shared-libraries.git`
   * Credentials: GitHub credentials if private
   * Include library changes in job recent changes: ✅
3. Use in Jenkinsfile:

```groovy
@Library('shared') _
```

---

## Screenshots

### 1️⃣ Prefect Flow Run
Captured after running the pipeline in Prefect UI, showing task completion and logging.

![Prefect Flow Run](https://github.com/user-attachments/assets/1b862f5b-0231-448b-9430-e619e36bddbe)

---

### 2️⃣ MLflow Experiment Dashboard
Shows all logged models, metrics (macro F1), and parameters for different vectorizers.

![MLflow Dashboard](https://github.com/user-attachments/assets/8272f6b2-d339-4453-994a-4d82f7cc5c5d)

---

### 3️⃣ Jenkins Pipeline Success
Jenkins build page showing successful stages, Docker build & push, and pipeline completion.

![Jenkins Success](https://github.com/user-attachments/assets/3f045e8f-0556-46db-9127-6011de92c7d9)




## Project Structure

```
LLM-2/
│
├─ src/
│   ├─ ingestion.py
│   ├─ preprocessor.py
│   ├─ vectorization.py
│   ├─ train.py
│
├─ Dataset/
├─ app.py
├─ flow.py
├─ requirements.txt
├─ start_services.sh
├─ Dockerfile
├─ Jenkinsfile
└─ README.md
```

---

## License

**MIT License** – see [LICENSE](LICENSE)

---

## Author

**Harshit Rai** – [GitHub](https://github.com/Harshitraiii2005)

```

