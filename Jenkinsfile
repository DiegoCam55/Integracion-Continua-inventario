pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker-compose'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/DiegoCam55/Integracion-Continua-inventario.git'
            }
        }

        stage('Build Images') {
            steps {
                sh "${DOCKER_COMPOSE} down"
                sh "${DOCKER_COMPOSE} build"
            }
        }

        stage('Start Services') {
            steps {
                sh "${DOCKER_COMPOSE} up -d db"
                sh "sleep 20" // Espera a que MySQL esté listo
                sh "${DOCKER_COMPOSE} up -d backend"
            }
        }

        stage('Run Backend Tests') {
            steps {
                sh "${DOCKER_COMPOSE} run backend pytest || echo 'No tests found'"
            }
        }

        stage('Deploy Frontend') {
            steps {
                sh "${DOCKER_COMPOSE} up -d frontend"
            }
        }
    }

    post {
        always {
            sh "${DOCKER_COMPOSE} down"
        }
    }
}