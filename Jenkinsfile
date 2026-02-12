pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/ashishbangar20/Ashish_oragneHRM_Automation.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Automation Tests') {
            steps {
                sh 'pytest'
            }
        }

    }
}
