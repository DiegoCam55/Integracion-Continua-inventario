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
                    # Ejecutar pytest con cobertura
                    ${DOCKER_COMPOSE} run --rm backend pytest --cov=. --cov-report=xml

                    # Copiar coverage.xml desde el contenedor al workspace
                    CONTAINER_ID=$(${DOCKER_COMPOSE} ps -q backend)
                    docker cp $CONTAINER_ID:/app/coverage.xml coverage.xml || true
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
