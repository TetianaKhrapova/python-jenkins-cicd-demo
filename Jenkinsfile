pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yourdockerhub/python-demo'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh script: """#!/bin/bash
                python3 -m venv pyenv
                source pyenv/bin/activate
                pip install flake8
                flake8 app.py
                """
            }
        }

        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest test_app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_IMAGE ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsID: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh 'echo $DOCKER_TOKEN | docker login -u yourdockerhub --password-stdin'
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }

        stage('Deploy (optional)') {
            steps {
                sh "docker run -d -p 8000:8000 $DOCKER_IMAGE"
            }
        }
    }
}
