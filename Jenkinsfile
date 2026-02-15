pipeline {

    agent any

    environment {
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

        // ================= Checkout =================
        stage('Checkout Code') {
            steps {
                echo "📥 Cloning Repository..."
                checkout scm
            }
        }

        // ================= Clean Old Container =================
        stage('Clean Old Container') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME || true'
            }
        }

        // ================= Build Docker Image =================
        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image..."
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        // ================= Run Tests =================
        stage('Run Tests in Docker') {
            steps {
                echo "🚀 Running Tests Inside Docker Container..."

                sh """
                mkdir -p $REPORT_DIR

                docker run --rm \
                --name $CONTAINER_NAME \
                -v \$(pwd)/$REPORT_DIR:/app/$REPORT_DIR \
                $IMAGE_NAME \
                pytest -n $WORKERS \
                --browser=$BROWSER \
                --headless=$HEADLESS \
                --html=$REPORT_DIR/report.html \
                --self-contained-html \
                -v
                """
            }
        }

        // ================= Publish Report =================
        stage('Publish HTML Report') {
            steps {
                echo "📊 Publishing HTML Report..."

                publishHTML([
                    allowMissing: false,
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
            echo "📦 Archiving Report..."
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
        }

        success {
            echo "✅ Automation Passed in Docker"
        }

        failure {
            echo "❌ Automation Failed in Docker"
        }
    }
}
