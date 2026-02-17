pipeline {

    agent any

    parameters {
        string(name: 'WORKERS', defaultValue: '4', description: 'Number of parallel workers')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Select browser')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression'], description: 'Select test suite to run')
    }

    environment {
        IMAGE_NAME = "ashish-orangehrm-automation"
        CONTAINER_NAME = "ashish-orangehrm-container"
        REPORT_DIR = "reports"
        EMAIL_RECIPIENT = "ashishbangar20@gmail.com"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        ansiColor('xterm')
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Clean Old Docker Container') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                sh '''
                mkdir -p $REPORT_DIR

                echo "Running Test Suite: ${TEST_SUITE}"
                echo "Browser: ${BROWSER}"
                echo "Workers: ${WORKERS}"

                docker run --rm \
                --name $CONTAINER_NAME \
                -v $(pwd)/$REPORT_DIR:/app/$REPORT_DIR \
                ${IMAGE_NAME}:${BUILD_NUMBER} \
                pytest -n ${WORKERS} \
                -m ${TEST_SUITE} \
                --browser=${BROWSER} \
                --headless=${HEADLESS} \
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
            sh 'docker rm -f $CONTAINER_NAME || true'
            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
        }

        success {
            emailext(
                subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build Successful 🎉

Job Name: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Test Suite: ${params.TEST_SUITE}
Browser: ${params.BROWSER}
Headless: ${params.HEADLESS}

HTML Report:
${env.BUILD_URL}HTML_20Report/

Console Output:
${env.BUILD_URL}console
""",
                to: "${EMAIL_RECIPIENT}",
                attachmentsPattern: 'reports/report.html'
            )
        }

        failure {
            emailext(
                subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build Failed ❌

Job Name: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Test Suite: ${params.TEST_SUITE}
Browser: ${params.BROWSER}
Headless: ${params.HEADLESS}

Check Console:
${env.BUILD_URL}console

HTML Report:
${env.BUILD_URL}HTML_20Report/
""",
                to: "${EMAIL_RECIPIENT}",
                attachmentsPattern: 'reports/report.html'
            )
        }
    }
}
