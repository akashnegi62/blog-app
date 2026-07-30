pipeline {

    agent any

    environment {

        IMAGE = "deepacode/blog-app:latest"

        STACK_NAME = "blog-app-stack"
        REGION = "ap-south-1"

    }

    stages {

        stage('Checkout Repository') {

            steps {

                checkout scm

            }

        }

        stage('Create / Update EC2') {

            steps {

                withAWS(credentials: 'aws-creds', region: "${REGION}") {

                    sh """
                    set -e

                    aws cloudformation deploy \
                        --stack-name ${STACK_NAME} \
                        --template-file cloudformation/ec2.yaml \
                        --parameter-overrides \
                            KeyName=jenkins-key \
                            InstanceType=t3.micro
                    """

                }

            }

        }

        stage('Wait for EC2') {

            steps {

                echo "Waiting for EC2 and Elastic IP..."

                sleep(time: 60, unit: 'SECONDS')

            }

        }

        stage('Get Elastic IP') {

            steps {

                withAWS(credentials: 'aws-creds', region: "${REGION}") {

                    script {

                        env.SERVER_IP = sh(
                            script: """
                            aws cloudformation describe-stacks \
                                --stack-name ${STACK_NAME} \
                                --query "Stacks[0].Outputs[?OutputKey=='ElasticIP'].OutputValue" \
                                --output text
                            """,
                            returnStdout: true
                        ).trim()

                        if (!env.SERVER_IP || env.SERVER_IP == "None") {
                            error("Elastic IP not found in CloudFormation outputs.")
                        }

                    }

                }

                echo "Elastic IP : ${SERVER_IP}"

            }

        }

        stage('Verify Application') {

            steps {

                sh '''
                set -e

                echo "Workspace"
                pwd

                echo ""
                ls -la

                echo ""

                if [ ! -f Dockerfile ]; then
                    echo "ERROR: Dockerfile not found."
                    exit 1
                fi

                echo "Dockerfile found."
                '''

            }

        }

        stage('Build Docker Image') {

            steps {

                sh """
                set -e

                docker build \
                    -t ${IMAGE} \
                    .
                """

            }

        }

        stage('Push Docker Image') {

            steps {

                withCredentials([

                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )

                ]) {

                    sh """
                    set -e

                    echo \$DOCKER_PASS | docker login \
                        -u \$DOCKER_USER \
                        --password-stdin

                    docker push ${IMAGE}

                    docker logout
                    """

                }

            }

        }

        stage('Wait for SSH') {

            steps {

                echo "Waiting for SSH..."

                sleep(time: 30, unit: 'SECONDS')

            }

        }

        stage('Install Docker on EC2') {

            steps {

                withCredentials([

                    sshUserPrivateKey(
                        credentialsId: 'ec2-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )

                ]) {

                    sh '''
                    set -e

                    ssh -i "$SSH_KEY" \
                        -o StrictHostKeyChecking=no \
                        "$SSH_USER@$SERVER_IP" << 'EOF'

                    set -e

                    if ! command -v docker >/dev/null 2>&1; then

                        echo "Installing Docker..."

                        sudo apt-get update

                        sudo apt-get install -y docker.io

                        sudo systemctl enable docker

                        sudo systemctl start docker

                        sudo usermod -aG docker ubuntu || true

                    else

                        echo "Docker already installed."

                    fi

                    sudo docker --version

EOF
                    '''

                }

            }

        }

        stage('Deploy to EC2') {

            steps {

                withCredentials([

                    sshUserPrivateKey(
                        credentialsId: 'ec2-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )

                ]) {

                    sh """
                    set -e

                    ssh -i "\$SSH_KEY" \
                        -o StrictHostKeyChecking=no \
                        "\$SSH_USER@${SERVER_IP}" << 'EOF'

                    set -e

                    echo "Pulling latest Docker image..."

                    sudo docker pull ${IMAGE}

                    echo "Stopping existing container..."

                    sudo docker stop blog_app || true

                    sudo docker rm blog_app || true

                    echo "Starting new container..."

                    sudo docker run -d \
                        --name blog_app \
                        --restart unless-stopped \
                        -p 3000:3000 \
                        ${IMAGE}

                    echo "Cleaning unused images..."

                    sudo docker image prune -f

                    echo ""
                    echo "Running Containers"

                    sudo docker ps

EOF
                    """

                }

            }

        }

    }

    post {

        success {

            echo "====================================="
            echo "Deployment Successful"
            echo "Elastic IP : ${SERVER_IP}"
            echo "Application URL : http://${SERVER_IP}:3000"
            echo "====================================="

        }

        failure {

            echo "====================================="
            echo "Deployment Failed"
            echo "====================================="

        }

    }

}