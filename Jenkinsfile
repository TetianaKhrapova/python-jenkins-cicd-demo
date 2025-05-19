pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'tkhrapova/python-demo'
    }

    stages {
        stage('Checkout') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: '7ec7817a-7c45-412f-9d61-664e064a6621', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        eval "$(ssh-agent -s)"
                        ssh-add $SSH_KEY
                        git checkout HEAD
                    '''
                }
            }
        }

        stage('Setup venv') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install flake8 pytest bump2version
                '''
            }
        }

        stage('Read Version') {
            steps {
                script {
                    def version = readFile('VERSION').trim()
                    env.DOCKER_TAGGED_IMAGE = "${DOCKER_IMAGE}:${version}"
                    echo "Docker image version tag: ${env.DOCKER_TAGGED_IMAGE}"
                }
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    flake8 app.py
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
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
                    sh '''
                        echo $DOCKER_TOKEN | docker login -u tkhrapova --password-stdin
                        docker push ${DOCKER_TAGGED_IMAGE}
                    '''
                }
            }
        }

        stage('Bump Version and Push') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: '7ec7817a-7c45-412f-9d61-664e064a6621', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        eval "$(ssh-agent -s)"
                        ssh-add $SSH_KEY
                        . .venv/bin/activate
                        git config user.name "jenkins"
                        git config user.email "jenkins@example.com"
                        bump2version patch --allow-dirty
                        git push origin HEAD:main
                    '''
                }
            }
        }
    }
}
