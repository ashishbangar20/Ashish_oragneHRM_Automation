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
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Verify Docker Connection') {
            steps {
                sh '''
                echo "Using Docker Host: $DOCKER_HOST"
                export DOCKER_HOST=$DOCKER_HOST
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
                sh '''
                export DOCKER_HOST=$DOCKER_HOST
                $DOCKER rm -f $CONTAINER_NAME || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                export DOCKER_HOST=$DOCKER_HOST
                $DOCKER build --no-cache -t $IMAGE_NAME .
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                sh '''
                export DOCKER_HOST=$DOCKER_HOST
                mkdir -p $REPORT_DIR

                $DOCKER run --rm \
                --name $CONTAINER_NAME \
                -v $(pwd)/$REPORT_DIR:/app/$REPORT_DIR \
                $IMAGE_NAME \
                pytest -n $WORKERS \
                --browser=$BROWSER \
                --headless=$HEADLESS \
                --html=$REPORT_DIR/report.html \
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
            sh '''
            export DOCKER_HOST=$DOCKER_HOST
            $DOCKER rm -f $CONTAINER_NAME || true
            '''
        }
    }
}
