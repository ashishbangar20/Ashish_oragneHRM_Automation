pipeline {

    agent any

    parameters {
        string(name: 'WORKERS', defaultValue: '4', description: 'Number of parallel workers')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Select browser')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
    }

    environment {
        DOCKER = "/usr/local/bin/docker"
        DOCKER_CONFIG = "${WORKSPACE}/.docker-temp"
        IMAGE_NAME = "orangehrm-automation"
        CONTAINER_NAME = "orangehrm-container"
        REPORT_DIR = "reports"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Prepare Clean Docker Config') {
            steps {
                sh '''
                mkdir -p $DOCKER_CONFIG
                echo '{}' > $DOCKER_CONFIG/config.json
                '''
            }
        }

        stage('Verify Docker') {
            steps {
                sh '$DOCKER --version'
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
                sh '$DOCKER build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                sh '''
                mkdir -p $REPORT_DIR

                $DOCKER run --rm \
                --name $CONTAINER_NAME \
                -v $(pwd)/$REPORT_DIR:/app/$REPORT_DIR \
                ${IMAGE_NAME}:${BUILD_NUMBER} \
                pytest -n ${params.WORKERS} \
                --browser=${params.BROWSER} \
                --headless=${params.HEADLESS} \
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
            sh '$DOCKER rm -f $CONTAINER_NAME || true'
        }

        success {
            echo "Build SUCCESS ✅"
        }

        failure {
            echo "Build FAILED ❌"
        }
    }
}
