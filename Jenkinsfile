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
                    echo '=== Ejecutando tests y generando coverage.xml hacia el workspace ==='
                    ${DOCKER_COMPOSE} run --rm -v ${WORKSPACE}:/workspace backend /bin/sh -c "pytest --cov=. --cov-report=xml && cp coverage.xml /workspace/coverage.xml"
                    echo '=== Listando coverage.xml en workspace ==='
                    ls -la ${WORKSPACE} || true
                """
            }
        }

           stage('Upload to Codecov') {
        steps {
            withCredentials([string(credentialsId: 'CODECOV_TOKEN', variable: 'CODECOV_TOKEN')]) {
                sh '''
                    echo "Subiendo coverage a Codecov desde Jenkins host..."
                    curl -s https://codecov.io/bash -o codecov.sh
                    bash codecov.sh -t $CODECOV_TOKEN -f ${WORKSPACE}/coverage.xml
                '''
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
