pipeline {
  agent any

  environment {
    // The Jenkins credential ID you stored for Docker Hub
    DOCKER_HUB_CREDENTIALS = 'dockerhub-final-proj'
    // Your Docker Hub repo
    DOCKER_IMAGE           = 'hamzah64/ml-ops-final-proj'
    IMAGE_TAG              = 'latest'
  }

  triggers {
    githubPush()
    pollSCM('H/5 * * * *')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', DOCKER_HUB_CREDENTIALS) {
            // This block logs in, then:
            // 1) pulls base images
            // 2) builds your image
            // 3) pushes it to Docker Hub
            def img = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
            img.push()
          }
        }
      }
    }
  }

  post {
    success {
      echo "✅ Image ${env.DOCKER_IMAGE}:${env.IMAGE_TAG} built & pushed."
    }
    failure {
      echo "❌ Build failed."
    }
  }
}
