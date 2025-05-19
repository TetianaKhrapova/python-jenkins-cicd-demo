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

        stage('Setup venv and install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate && pip install --upgrade pip
                    . .venv/bin/activate && pip install -r requirements.txt flake8 pytest bump2version
                '''
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
                sh '. .venv/bin/activate && flake8 app.py'
            }
        }

        stage('Test') {
            steps {
                sh '. .venv/bin/activate && pytest test_app.py'
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
                sh '''
                    . .venv/bin/activate && bump2version patch --allow-dirty
                    git config user.name "jenkins"
                    git config user.email "jenkins@example.com"
                    git push origin HEAD:main
                '''
            }
        }

        // За потреби можна розкоментувати стадію деплою
        // stage('Deploy (optional)') {
        //     steps {
        //         sh "docker run -d -p 8000:8000 ${env.DOCKER_TAGGED_IMAGE}"
        //     }
        // }
    }
}
