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
#!/bin/bash
set -e
echo "Running pytest with coverage inside backend container..."

# Ejecutar tests montando el directorio de Jenkins como volumen
docker compose run --rm -v $PWD:/app backend /bin/bash -c "pytest --maxfail=1 --disable-warnings -q --cov=. --cov-report=xml"

# Ahora coverage.xml ya está en el workspace de Jenkins
if [ -f coverage.xml ]; then
    echo "Uploading coverage.xml to Codecov..."
    bash <(curl -s https://codecov.io/bash) -f coverage.xml -t ${CODECOV_TOKEN} || echo "Codecov upload failed"
else
    echo "coverage.xml not found, skipping Codecov upload"
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
