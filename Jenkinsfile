pipeline {

    agent any

    parameters {
        string(name: 'WORKERS', defaultValue: '4', description: 'Number of parallel workers')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Select browser')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression'], description: 'Select test suite to run')
    }

    environment {
        DOCKER = "/usr/local/bin/docker"
        DOCKER_HOST = "unix:///Users/ashish/.docker/run/docker.sock"
        DOCKER_CONFIG = "${WORKSPACE}/.docker-temp"
        IMAGE_NAME = "ashish-orangehrm-automation"
        CONTAINER_NAME = "ashish-orangehrm-container"
        REPORT_DIR = "reports"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Prepare Docker Environment') {
            steps {
                sh """
                mkdir -p $DOCKER_CONFIG
                echo '{}' > $DOCKER_CONFIG/config.json
                export DOCKER_HOST=$DOCKER_HOST
                $DOCKER --version
                """
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Clean Old Container') {
            steps {
                sh """
                export DOCKER_HOST=$DOCKER_HOST
                $DOCKER rm -f $CONTAINER_NAME || true
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                export DOCKER_HOST=$DOCKER_HOST
                $DOCKER build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                """
            }
        }

        stage('Run Tests in Docker') {
            steps {
                sh """
                export DOCKER_HOST=$DOCKER_HOST
                mkdir -p $REPORT_DIR

                echo "Running Test Suite: ${params.TEST_SUITE}"

                $DOCKER run --rm \
                --name $CONTAINER_NAME \
                -v \$(pwd)/$REPORT_DIR:/app/$REPORT_DIR \
                ${IMAGE_NAME}:${BUILD_NUMBER} \
                pytest -n ${params.WORKERS} \
                -m ${params.TEST_SUITE} \
                --browser=${params.BROWSER} \
                --headless=${params.HEADLESS} \
                --html=$REPORT_DIR/report.html \
                --self-contained-html \
                -v
                """
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
        sh """
        export DOCKER_HOST=$DOCKER_HOST
        $DOCKER rm -f $CONTAINER_NAME || true
        """
    }

    success {
        emailext(
            subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
Build Successful

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Test Suite: ${params.TEST_SUITE}
Browser: ${params.BROWSER}

Console:
${env.BUILD_URL}console
""",
            to: "ashishbangar20@gmail.com"
        )
    }

    failure {
        emailext(
            subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
Build Failed

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Test Suite: ${params.TEST_SUITE}
Browser: ${params.BROWSER}

Console:
${env.BUILD_URL}console
""",
            to: "ashishbangar20@gmail.com"
        )
    }
}

