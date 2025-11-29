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
            
sh """
echo "Running pytest with coverage inside backend container..."

# Ejecutar los tests dentro del contenedor backend
docker compose run --name ci_backend backend /bin/sh -c "pytest --maxfail=1 --disable-warnings -q --cov=. --cov-report=xml"
docker cp ci_backend:/app/coverage.xml coverage.xml
docker rm ci_backend
"""

# Subir a Codecov si coverage.xml existe
if [ -f coverage.xml ]; then
    echo "Uploading coverage.xml to Codecov..."
    bash <(curl -s https://codecov.io/bash) -f coverage.xml -t ${CODECOV_TOKEN} || echo "Codecov upload failed"
else
    echo "coverage.xml not found, skipping Codecov upload"
fi
           
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
