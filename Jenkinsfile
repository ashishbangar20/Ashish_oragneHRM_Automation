pipeline {

    agent any

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
                pytest --html=$REPORT_DIR/report.html --self-contained-html
                '''
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Automation Report'
                ])
            }
        }
    }
}
