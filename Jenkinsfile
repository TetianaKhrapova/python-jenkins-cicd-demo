pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'tkhrapova/python-demo'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup venv') {
            steps {
                sh """
                    python3 -m venv .venv
                    source .venv/bin/activate
                    pip install --upgrade pip
                    pip install flake8 pytest bump2version
                """
            }
        }

        stage('Read Version') {
            steps {
                script {
                    VERSION = readFile('VERSION').trim()
                    env.DOCKER_TAGGED_IMAGE = "${DOCKER_IMAGE}:${VERSION}"
                    echo "Docker image version tag: ${env.DOCKER_TAGGED_IMAGE}"
                }
            }
        }

        stage('Lint') {
            steps {
                sh """
                    source .venv/bin/activate
                    flake8 app.py
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    source .venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${env.DOCKER_TAGGED_IMAGE} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh 'echo $DOCKER_TOKEN | docker login -u tkhrapova --password-stdin'
                    sh "docker push ${env.DOCKER_TAGGED_IMAGE}"
                }
            }
        }

        stage('Bump Version') {
            steps {
                sh """
                    source .venv/bin/activate
                    bump2version patch --allow-dirty
                    git config user.name "jenkins"
                    git config user.email "jenkins@example.com"
                    git commit -am "Bump version [ci skip]"
                    git push origin HEAD:main
                """
            }
        }

        // stage('Deploy (optional)') {
        //     steps {
        //         sh "docker run -d -p 8000:8000 ${env.DOCKER_TAGGED_IMAGE}"
        //     }
        // }
    }
}
