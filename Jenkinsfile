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
                sh 'pwd'
            }
        }

        stage('Clear Old Setup Files') {
            steps {
                script {
                    try {
                        sh 'rm cert.pem priv_key.pem'
                        echo 'Old certificates removed'
                    } catch (err) {
                        echo 'No old certificates found'
                    }
                    try {
                        sh 'rm docker-compose.yml'
                        echo 'Old docker-compose.yml removed'
                    } catch (err) {
                        echo 'No old docker-compose.yml found'
                    }
                }
            }
        }

        stage('Download Setup Files') {
            steps {
                withAWS(region: 'eu-west-2', credentials: env.AWS_CREDENTIALS) {
                    s3Download(bucket: 'animal-repo-bucket', file:'cert.pem')
                    s3Download(bucket: 'animal-repo-bucket', file:'priv_key.pem')
                    s3Download(bucket: 'animal-repo-bucket', file:'docker-compose.yml')
                }
            }
        }

        stage('Unpack Setup Files') {
            steps {
                sh '''
                mv cert.pem cert
                mv priv_key.pem key
                mv docker-compose.yml docker-compose-dir
                mv cert/cert.pem .
                mv key/priv_key.pem .
                mv docker-compose-dir/docker-compose.yml .
                rm -r cert key docker-compose-dir
                '''
            }
        }

        stage('Deploy to EC2') {
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