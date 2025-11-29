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
            sh """
            # Ejecutar pytest con cobertura dentro del contenedor backend
            #${DOCKER_COMPOSE} run --rm backend pytest --cov=. --cov-report=xml
            docker compose run --rm backend pytest /app/tests -q --maxfail=1 --disable-warnings


            # Obtener el ID del contenedor backend ya iniciado
            CONTAINER_ID=`${DOCKER_COMPOSE} ps -q backend`

            # Copiar coverage.xml al workspace de Jenkins
            docker cp \$CONTAINER_ID:/app/coverage.xml coverage.xml || true
        """
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
