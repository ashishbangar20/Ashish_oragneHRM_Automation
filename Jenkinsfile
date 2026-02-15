pipeline {

    agent any

    environment {
        DOCKER = "/usr/local/bin/docker"
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

        stage('Checkout Code') {
            steps {
                echo "📥 Cloning Repository..."
                checkout scm
            }
        }

        stage('Clean Old Container') {
            steps {
                sh '''
                $DOCKER rm -f $CONTAINER_NAME || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image..."
                sh '''
                $DOCKER build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                echo "🚀 Running Tests Inside Docker..."
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
            echo "📦 Archiving Report..."
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
            sh '$DOCKER rm -f $CONTAINER_NAME || true'
        }

        success {
            echo "✅ Automation Passed in Docker"
        }

        failure {
            echo "❌ Automation Failed in Docker"
        }
    }
}
