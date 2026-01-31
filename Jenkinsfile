@Library('shared') _

pipeline {
    agent any

    environment {
        IMAGE_NAME = "llm"
        DOCKER_USERNAME = "harshitrai20"
    }

    stages {

        stage("Workspace Cleanup") {
            steps {
                cleanWs()
            }
        }

        stage("Environment Setup") {
            steps {
                sh '''
                #!/bin/bash
                python3 -m venv .venv
                source .venv/bin/activate
                pip install -r requirements.txt
                '''

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
            echo " Pipeline failed"
        }
    }
}
