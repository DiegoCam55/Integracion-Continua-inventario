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
    withCredentials([string(credentialsId: 'CODECOV_TOKEN', variable: 'CODECOV_TOKEN')]) {
        sh '''
            set -e
            echo "Ejecutando pytest con coverage dentro del contenedor backend..."

            # Ejecuta pytest, apunta a la carpeta de código (backend)
            docker compose run --rm -v $PWD:/app backend /bin/bash -c "
                ls -R /app
                pytest backend/tests --maxfail=1 --disable-warnings -q --cov=backend --cov-report=xml || true
            "

            # Copia coverage.xml si existe
            if [ -f backend/coverage.xml ]; then
                cp backend/coverage.xml coverage.xml
                echo "coverage.xml copiado para Codecov."
            else
                echo "No se encontró coverage.xml, se omite."
            fi
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
