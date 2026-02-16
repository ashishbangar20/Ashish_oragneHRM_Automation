pipeline {

    agent any

    environment {
        DOCKER = "/usr/local/bin/docker"
        DOCKER_HOST = "unix:///Users/ashish/.docker/run/docker.sock"
        IMAGE_NAME = "orangehrm-automation"
        CONTAINER_NAME = "orangehrm-container"
        REPORT_DIR = "reports"
        WORKERS = "4"
        BROWSER = "chrome"
        HEADLESS = "true"
    }

    options {
        timestamps()
    }

    stages {

        stage('Verify Docker Connection') {
            steps {
                sh '''
                echo "Docker Host: $DOCKER_HOST"
                $DOCKER context use desktop-linux
                $DOCKER info
                '''
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Clean Old Container') {
            steps {
                sh '$DOCKER rm -f $CONTAINER_NAME || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '$DOCKER build -t $IMAGE_NAME .'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                sh '''
                mkdir -p $REPORT_DIR

                $DOCKER run --name $CONTAINER_NAME \
                -v $(pwd)/reports:/app/reports \
                $IMAGE_NAME \
                pytest -n $WORKERS \
                --browser=$BROWSER \
                --headless=$HEADLESS \
                --html=reports/report.html \
                --self-contained-html \
                -v
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'OrangeHRM Automation Report'
                ])
            }
        }
    }

    post {
        always {
            sh '$DOCKER rm -f $CONTAINER_NAME || true'
        }
    }
}
