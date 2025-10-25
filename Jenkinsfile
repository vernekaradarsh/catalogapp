pipeline {
  agent any

  environment {
    IMAGE_NAME = "catalogapp"
    IMAGE_TAG = "optimized"
    EC2_USER = "ubuntu"
    EC2_IP = "your-ec2-ip"   // Replace with your actual EC2 public IP or DNS
    CREDENTIALS_ID = "ec2-ssh"
    APP_DIR = "catalogapp"   // Subdirectory where manage.py lives
  }

  stages {
    stage('Checkout') {
      steps {
        echo "🔍 Checking out source code..."
        git url: 'https://github.com/vernekaradarsh/catalogapp.git', branch: 'main'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          def app = docker.build("${IMAGE_NAME}")
          app.tag("${IMAGE_TAG}")
          app.tag("latest")
        }
      }
    }

    stage('Run Tests & Coverage') {
      steps {
        echo "🧪 Running tests and generating coverage..."
        sh '''
        docker run --rm \
          -v $PWD/${APP_DIR}:/app \
          -w /app \
          ${IMAGE_NAME}:${IMAGE_TAG} /bin/bash -c "
            coverage run manage.py test &&
            coverage report -m > coverage.txt &&
            coverage html
          "
        '''
      }
    }

    stage('Deploy to EC2') {
      steps {
        echo "🚀 Deploying to AWS EC2..."
        withCredentials([sshUserPrivateKey(credentialsId: "${CREDENTIALS_ID}", keyFileVariable: 'KEY')]) {
          sh '''
          ssh -i $KEY -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "
            docker pull ${IMAGE_NAME}:latest || true &&
            docker stop app || true &&
            docker rm app || true &&
            docker run -d --name app -p 8000:8000 -v ~/media:/app/media ${IMAGE_NAME}:latest &&
            sudo systemctl restart nginx
          "
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ Build & Deploy Successful!"
      archiveArtifacts artifacts: "${APP_DIR}/coverage.txt", allowEmptyArchive: true
      publishHTML(target: [
        allowMissing: true,
        keepAll: true,
        alwaysLinkToLastBuild: true,
        reportDir: "${APP_DIR}/htmlcov",
        reportFiles: 'index.html',
        reportName: 'Coverage Report'
      ])
    }

    failure {
      echo "❌ Build or Deployment Failed — Check Jenkins logs for details."
    }
  }
}
