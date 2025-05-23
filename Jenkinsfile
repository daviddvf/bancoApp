pipeline {
  agent any

  environment {
    IMAGE_NAME = "daviddvf/banco_app"
    IMAGE_TAG  = "web"
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/daviddvf/bancoApp.git',
            branch: 'main',
            credentialsId: 'git-creds'
      }
    }

    stage('Build & Push') {
      steps {
        script {
          
          docker.build("${IMAGE_NAME}:${IMAGE_TAG}", "-f banco/Dockerfile banco")
          
          
          docker.withRegistry('https://index.docker.io/v1/', 'docker-creds') {
            def img = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
            img.push()           
            img.push('latest')   
          }
        }
      }
    }

    stage('Deploy with Compose') {
      steps {
        
        withCredentials([
          usernamePassword(
            credentialsId: 'docker-creds',
            usernameVariable: 'DOCKERHUB_USR',
            passwordVariable: 'DOCKERHUB_PSW'
          )
        ]) {
          sh 'echo $DOCKERHUB_PSW | docker login --username $DOCKERHUB_USR --password-stdin'
        }

        
        
        dir('banco') {
          sh 'docker compose pull'
          sh 'docker compose down'
          sh 'docker compose up -d --build'
           }
      }
    }
  }

  post {
    success { echo "✅ Build, push y deploy completados con éxito  " }
    failure { echo "❌ Hubo un fallo en el pipeline" }
    always  { sh 'docker logout || true' }
  }
}
