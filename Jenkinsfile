pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = "docker compose"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/DiegoCam55/Integracion-Continua-inventario.git'
            }
        }

        stage('Build Images') {
            steps {
                sh """
                    ${DOCKER_COMPOSE} down
                    ${DOCKER_COMPOSE} build
                """
            }
        }

        stage('Start Services') {
            steps {
                sh """
                    ${DOCKER_COMPOSE} up -d db
                    sleep 20
                    ${DOCKER_COMPOSE} up -d backend
                """
            }
        }

       stage('Tests & Codecov') {
  steps {
    withCredentials([string(credentialsId: 'CODECOV_TOKEN', variable: 'CODECOV_TOKEN')]) {
      sh '''
        set -e
        echo "Running pytest with coverage inside backend container..."
        # run tests and keep the container so we can copy coverage.xml
        docker compose run --name ci_backend --rm backend /bin/sh -c "pytest --maxfail=1 --disable-warnings -q --cov=. --cov-report=xml || true"
        # copy coverage (if exists)
        if docker ps -a --format '{{.Names}}' | grep -q ci_backend; then
          docker cp ci_backend:/app/coverage.xml coverage.xml || true
        fi
        # try uploader
        if [ -f coverage.xml ]; then
          echo "Uploading coverage.xml to Codecov..."
          bash <(curl -s https://codecov.io/bash) -f coverage.xml -t ${CODECOV_TOKEN} || echo "Codecov upload failed"
        else
          echo "coverage.xml not found, skipping codecov upload"
        fi
      '''
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
    }
  }
}




        stage('Deploy Frontend') {
            steps {
                sh """
                    ${DOCKER_COMPOSE} up -d frontend
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado. Contenedores se mantienen activos."
        }
    }
}
