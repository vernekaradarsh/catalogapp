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
        sshagent(['ec2-ssh']) {
          sh '''
            ssh -o StrictHostKeyChecking=no ubuntu@13.232.196.111 "
              cd ~/catalogapp &&
              git pull &&
              docker build -t catalogapp . &&
              docker stop app || true &&
              docker rm app || true &&
              docker run -d --name app -p 8000:8000 -v ~/media:/app/media catalogapp &&
              sudo nginx -s reload
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
