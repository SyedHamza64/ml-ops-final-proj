pipeline {
  agent any

  environment {
    // The Jenkins credential ID you stored for Docker Hub
    DOCKER_HUB_CREDENTIALS = 'dockerhub-final-proj'
    // Your Docker Hub repo
    DOCKER_IMAGE           = 'hamzah64/ml-ops-final-proj'
    IMAGE_TAG              = 'latest'
  }

  // We'll rely on GitHub webhooks + GitHub hook trigger for SCM polling
  triggers {
    pollSCM('H/5 * * * *')
  }

  stages {
    stage('Validate PR Target') {
      // Only run on Pull Requests into "test"
      when {
        allOf {
          expression { env.CHANGE_ID }          // it is a PR
          changeRequest target: 'test'         // target branch is 'test'
        }
      }
      steps {
        echo "🔍 Detected PR #${env.CHANGE_ID} → ${env.CHANGE_TARGET}"
      }
    }

    stage('Checkout') {
      when { changeRequest target: 'test' }
      steps {
        checkout scm
      }
    }

    stage('Fetch Data') {
      when { changeRequest target: 'test' }
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
      when { changeRequest target: 'test' }
      steps {
        script {
          docker.build("${env.DOCKER_IMAGE}:${env.IMAGE_TAG}")
        }
      }
    }

    stage('Push to Docker Hub') {
      when { changeRequest target: 'test' }
      steps {
        // Inject your Docker Hub creds and push
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
      echo "✅ PR #${env.CHANGE_ID} built & Docker image pushed successfully"
    }
    failure {
      echo "❌ PR #${env.CHANGE_ID} build failed"
    }
  }
}
