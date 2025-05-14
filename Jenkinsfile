pipeline {
  agent any

  environment {
    DOCKER_HUB_CREDENTIALS = 'dockerhub-final-proj'
    DOCKER_IMAGE           = 'hamzah64/ml-ops-final-proj'
    IMAGE_TAG              = 'latest'
  }

  triggers {
    githubPush()           // GitHub webhooks
    pollSCM('H/5 * * * *') // fallback polling
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build("${env.DOCKER_IMAGE}:${env.IMAGE_TAG}")
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: env.DOCKER_HUB_CREDENTIALS,
          usernameVariable: 'DOCKERHUB_USER',
          passwordVariable: 'DOCKERHUB_PASS'
        )]) {
          sh """
            docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASS
            docker push ${env.DOCKER_IMAGE}:${env.IMAGE_TAG}
          """
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
