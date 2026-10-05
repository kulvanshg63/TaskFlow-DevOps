pipeline {

    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Starting TaskFlow build...'

                bat 'python --version'
                bat 'pip install -r requirements.txt'

                echo 'Build completed successfully.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'

                bat 'pytest'

                echo 'All tests completed.'
            }
        }

        stage('Package') {
            steps {
                echo 'Packaging TaskFlow application...'

                bat 'if exist taskflow-package.zip del taskflow-package.zip'

                bat 'powershell -Command "Compress-Archive -Path app.py,database.py,requirements.txt,Jenkinsfile,templates,static -DestinationPath taskflow-package.zip -Force"'

                echo 'Package created successfully.'
            }
        }

    }

    post {

        success {
            echo 'TaskFlow CI Pipeline completed successfully!'
        }

        failure {
            echo 'TaskFlow CI Pipeline failed.'
        }

    }
}