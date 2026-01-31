@Library('shared') _

pipeline {
    agent any

    environment {
        IMAGE_NAME = "llm"
        DOCKER_USERNAME = "harshitrai20"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Workspace Cleanup") {
            steps {
                cleanWs()
                checkout scm
            }
        }

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

        stage("Start Services (MLflow + Prefect)") {
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
            steps {
                script {
                    docker_build(
                        env.DOCKER_USERNAME,
                        env.IMAGE_NAME,
                        "latest"
                    )
                }
            }
        }

        stage("Push Docker Image to DockerHub") {
            steps {
                script {
                    docker_push(
                        env.DOCKER_USERNAME,
                        env.IMAGE_NAME,
                        "latest"
                    )
                }
            }
        }
    }

    post {
        success {
            echo "Image pushed to DockerHub successfully"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
