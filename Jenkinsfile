pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/yourusername/catalogapp.git'
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t catalogapp:latest .'
            }
        }
        stage('Test in Container') {
            steps {
                sh '''
                docker run --rm catalogapp:latest python manage.py test catalogues -v
                docker run --rm catalogapp:latest coverage run manage.py test
                coverage html
                coverage report -m
                '''
            }
        }
        stage('Deploy to EC2') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh', keyFileVariable: 'KEY')]) {
                    sh '''
                    ssh -i $KEY -o StrictHostKeyChecking=no ubuntu@your-ec2-ip "
                    docker pull catalogapp:latest &&
                    docker stop app || true &&
                    docker rm app || true &&
                    docker run -d --name app -p 8000:8000 -v ~/media:/app/media catalogapp:latest &&
                    sudo nginx -s reload"
                    '''
                }
            }
        }
    }
    post {
        success {
            publishHTML([reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'Coverage Report'])
        }
        failure {
            echo 'Build Failed — check Jenkins logs'
        }
    }
}
