pipeline {
  agent any

  environment {
    IMAGE_NAME = "catalogapp"
    IMAGE_TAG = "optimized"
    EC2_USER = "ubuntu"
    EC2_IP = "your-ec2-ip"   // Replace with your actual EC2 public IP or DNS
    CREDENTIALS_ID = "ec2-ssh"
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

    stage('Run Tests') {
      steps {
        echo "🧪 Running Django tests..."
        sh '''
        docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python3 manage.py test catalogues -v 2
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
    }
    failure {
      echo "❌ Build or Deployment Failed — Check Jenkins logs for details."
    }
  }
}
