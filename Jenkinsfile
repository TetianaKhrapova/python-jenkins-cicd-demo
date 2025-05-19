pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'tkhrapova/python-demo'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code using SSH key
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
                // Setup Python virtual environment and install dependencies
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
                    // Read version from file and set Docker image tag
                    def version = readFile('VERSION').trim()
                    env.DOCKER_TAGGED_IMAGE = "${DOCKER_IMAGE}:${version}"
                    echo "Docker image version tag: ${env.DOCKER_TAGGED_IMAGE}"
                }
            }
        }

        stage('Lint') {
            steps {
                // Run code linting with flake8
                sh '''
                    . .venv/bin/activate
                    flake8 app.py
                '''
            }
        }

        stage('Test') {
            steps {
                // Run tests with pytest
                sh '''
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build Docker image tagged with current version
                sh "docker build -t ${env.DOCKER_TAGGED_IMAGE} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Push the Docker image to Docker Hub using token authentication
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
                // Bump patch version only if the git tag does not already exist
                withCredentials([sshUserPrivateKey(credentialsId: '7ec7817a-7c45-412f-9d61-664e064a6621', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        eval "$(ssh-agent -s)"
                        ssh-add $SSH_KEY
                        . .venv/bin/activate

                        git config user.name "jenkins"
                        git config user.email "jenkins@example.com"

                        CURRENT_VERSION=$(cat VERSION)          # Read version WITHOUT leading 'v'
                        TAG="v${CURRENT_VERSION}"               # Prepend 'v' to form git tag name

                        # Check if tag already exists to avoid bump2version error
                        if git rev-parse "$TAG" >/dev/null 2>&1; then
                            echo "Tag $TAG already exists. Skipping bump and tag creation."
                        else
                            bump2version patch --allow-dirty
                            git push origin HEAD:main --tags
                        fi
                    '''
                }
            }
        }
    }
}
