pipeline {

    agent any

    environment {
        DOCKER = "/usr/local/bin/docker"
        DOCKER_CONFIG_DIR = "/tmp/docker-config"
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

        stage('Prepare Docker Environment') {
            steps {
                echo "🧹 Preparing Clean Docker Config..."
                sh '''
                rm -rf $DOCKER_CONFIG_DIR
                mkdir -p $DOCKER_CONFIG_DIR
                '''
            }
        }

        stage('Clean Old Container') {
            steps {
                sh '''
                export DOCKER_CONFIG=$DOCKER_CONFIG_DIR
                $DOCKER rm -f $CONTAINER_NAME || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image..."
                sh '''
                export DOCKER_CONFIG=$DOCKER_CONFIG_DIR
                $DOCKER build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                echo "🚀 Running Tests Inside Docker..."
                sh '''
                export DOCKER_CONFIG=$DOCKER_CONFIG_DIR
                mkdir -p $REPORT_DIR

                $DOCKER run --name $CONTAINER_NAME \
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
            echo "📦 Archiving Report..."
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
            sh '''
            export DOCKER_CONFIG=$DOCKER_CONFIG_DIR
            $DOCKER rm -f $CONTAINER_NAME || true
            '''
        }

        success {
            echo "✅ Automation Passed in Docker"
        }

        failure {
            echo "❌ Automation Failed in Docker"
        }
    }
}
