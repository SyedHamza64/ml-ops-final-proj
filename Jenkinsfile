pipeline {
  agent any

  environment {
    DOCKER_HUB_CREDENTIALS = 'dockerhub-final-proj'
    DOCKER_IMAGE           = 'hamzah64/ml-ops-final-proj'
    IMAGE_TAG              = 'latest'
  }

  triggers {
    githubPush()           // React to GitHub push & PR webhooks
    pollSCM('H/5 * * * *') // Fallback polling every 5 minutes
  }

  stages {
    stage('Checkout') {
      when {
        anyOf {
          branch 'dev'
          changeRequest target: 'test'
        }
      }
      steps {
        checkout scm
      }
    }

    stage('Fetch Data') {
      when {
        anyOf {
          branch 'dev'
          changeRequest target: 'test'
        }
      }
      steps {
        script {
          if (isUnix()) {
            sh 'python3 -m pip install --upgrade pip'
            sh 'python3 -m pip install -r requirements.txt dvc'
            sh 'dvc pull'
          } else {
            bat 'python -m pip install --upgrade pip'
            bat 'python -m pip install -r requirements.txt dvc'
            bat 'python -m dvc pull'
          }
        }
      }
    }

    stage('Build Docker Image') {
      when {
        anyOf {
          branch 'dev'
          changeRequest target: 'test'
        }
      }
      steps {
        script {
          docker.build("${env.DOCKER_IMAGE}:${env.IMAGE_TAG}")
        }
      }
    }

    stage('Push to Docker Hub') {
      when {
        anyOf {
          branch 'dev'
          changeRequest target: 'test'
        }
      }
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
