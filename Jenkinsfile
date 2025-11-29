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

       stage('Run Backend Tests') {
  steps {
    // Ejecuta pytest dentro de un contenedor que monta el workspace de Jenkins
    // de modo que coverage.xml quede disponible en el workspace al terminar.
    sh """
      echo '=== Ejecutando tests y generando coverage.xml hacia el workspace ==='
      ${DOCKER_COMPOSE} run --rm -v ${WORKSPACE}:/workspace backend /bin/sh -c "pytest --cov=. --cov-report=xml && cp coverage.xml /workspace/coverage.xml"
      echo '=== Listando coverage.xml en workspace ==='
      ls -la ${WORKSPACE} || true
    """
  }
}
    stage('Upload to Codecov') {
    withCredentials([string(credentialsId: 'CODECOV_TOKEN', variable: 'CODECOV_TOKEN')]) {
        sh '''
            echo "Subiendo coverage a Codecov..."
            docker compose run --rm -v $PWD:/workspace backend /bin/bash -c "
                bash <(curl -s https://codecov.io/bash) -t $CODECOV_TOKEN -f /workspace/coverage.xml
            "
        '''
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
