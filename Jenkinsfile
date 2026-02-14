pipeline {

    agent any

    environment {
        VENV = "venv"
        REPORT_DIR = "reports"
        BROWSER = "chrome"
        HEADLESS = "true"
        WORKERS = "4"      // 👈 Parallel threads count
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // ================= Checkout Code =================
        stage('Checkout Code') {
            steps {
                echo "Cloning Git Repository..."
                checkout scm
            }
        }

        // ================= Setup Python Environment =================
        stage('Setup Python Environment') {
            steps {
                echo "Creating Virtual Environment & Installing Dependencies..."
                sh '''
                python3 -m venv $VENV
                . $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        // ================= Run Automation Tests =================
        stage('Run Automation Tests') {
            steps {
                echo "Executing Pytest Automation in Headless + Parallel Mode..."
                sh '''
                . $VENV/bin/activate
                mkdir -p $REPORT_DIR

                pytest \
                -n $WORKERS \
                --dist=loadfile \
                --browser=$BROWSER \
                --headless=$HEADLESS \
                --html=$REPORT_DIR/report.html \
                --self-contained-html \
                -v
                '''
            }
        }

        // ================= Publish HTML Report =================
        stage('Publish Test Report') {
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

    // ================= Post Build Actions =================
    post {

        always {
            echo "Archiving Reports..."
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
        }

        success {
            echo "✅ Automation Tests Passed Successfully"
        }

        failure {
            echo "❌ Automation Tests Failed"
        }

        cleanup {
            echo "Cleaning Workspace..."
            cleanWs()
        }
    }
}
