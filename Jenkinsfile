pipeline {

    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    environment {
        VENV = "venv"
        REPORT_DIR = "reports"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv $VENV
                source $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automation Tests') {
            steps {
                sh '''
                source $VENV/bin/activate
                pytest -n 2 --html=$REPORT_DIR/report.html --self-contained-html
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Automation Test Report'
                ])
            }
        }

    }

    post {

        always {
            echo "Build Completed"
        }

        success {
            echo "Automation Tests Passed"
        }

        failure {
            echo "Automation Tests Failed"
        }

        cleanup {
            cleanWs()
        }
    }
}
