pipeline {
    agent any

    environment {
        GIT_CREDENTIALS = 'Github'
        AWS_CREDENTIALS = 'ec2-user'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: env.GIT_CREDENTIALS, url: 'https://github.com/TobyJWalker/animal-tracker.git'
            }
        }

        stage('Deploy to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: env.AWS_CREDENTIALS, secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    sh '''
                    docker-compose down
                    docker-compose build
                    docker-compose up -d
                    '''
                }
            }
        }
    }
}