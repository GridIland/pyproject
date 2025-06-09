pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
    timeout(time: 15, unit: 'MINUTES')
    timestamps()
  }

  environment {
    APP_NAME = "demo-app"
    BRANCH_NAME = env.BRANCH_NAME.replaceAll('/', '-')
    TEAM_EMAIL = 'koussougboss@gmail.com, huguesblakime@gmail.com'
    PYTHONPATH = "${WORKSPACE}"
  }

  stages {
    // Étape 1: Préparation
    stage('Checkout & Setup') {
      agent {
        dockerContainer {
          image 'icontain/jenkins-node-agent:latest'
        }
      }
      steps {
        checkout scm
        sh '''
          python -m pip install --upgrade pip
          pip install -r dev-requirements.txt
        '''
      }
    }

    // Étape 2: Qualité de code
    stage('Quality & Test') {
      parallel {
        stage('Code Quality') {
          agent {
            dockerContainer {
              image 'icontain/jenkins-node-agent:latest'
            }
          }
          steps {
            checkout scm
            sh '''
              python -m pip install --upgrade pip
              pip install -r dev-requirements.txt
              pip install flake8 black isort mypy
            '''
            // Formatage du code
            sh 'black --check . || echo "Code formatting issues found"'
            // Vérification des imports
            sh 'isort --check-only . || echo "Import sorting issues found"'
            // Linting avec flake8
            sh 'flake8 . || echo "Linting issues found"'
            // Vérification des types (optionnel)
            sh 'mypy . || echo "Type checking issues found"'
          }
          post {
            failure {
              emailext body: "Code quality checks failed in build ${env.BUILD_NUMBER}\n${env.BUILD_URL}",
                      subject: "FAILED: Code Quality - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                      to: "${TEAM_EMAIL}"
            }
          }
        }
        stage('Unit Tests') {
          agent {
            dockerContainer {
              image 'icontain/jenkins-node-agent:latest'
            }
          }
          steps {
            checkout scm
            sh '''
              python -m pip install --upgrade pip
              pip install -r dev-requirements.txt
              pip install pytest pytest-cov pytest-xvfb
            '''
            // Exécution des tests avec couverture
            sh 'pytest --cov=. --cov-report=xml --cov-report=html --junitxml=test-results.xml'
          }
          post {
            always {
              publishTestResults testResultsPattern: 'test-results.xml'
              publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
            }
            failure {
              emailext body: "Unit tests failed in build ${env.BUILD_NUMBER}\n${env.BUILD_URL}",
                      subject: "FAILED: Tests - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                      to: "${TEAM_EMAIL}"
            }
          }
        }
      }
    }

    // Étape 3: Build et Package
    stage('Build & Package') {
      when { branch 'develop' }
      agent {
        dockerContainer {
          image 'icontain/jenkins-node-agent:latest'
        }
      }
      steps {
        checkout scm
        sh '''
          python -m pip install --upgrade pip
          pip install build wheel
          python -m build
        '''
        archiveArtifacts artifacts: 'dist/*', fingerprint: true
      }
    }

    // Étape 4: Build Docker Image
    stage('Build Docker Image') {
      when { branch 'develop' }
      agent {
        docker {
          image 'docker:24-cli'
          args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
        sh 'docker build -t ${APP_NAME}:${BRANCH_NAME}-${BUILD_NUMBER} .'
        sh 'docker tag ${APP_NAME}:${BRANCH_NAME}-${BUILD_NUMBER} ${APP_NAME}:latest'
      }
    }

    // Étape 5: Security Scan (optionnel)
    stage('Security Scan') {
      when { branch 'develop' }
      agent {
        docker {
          image 'python:3.11-slim'
        }
      }
      steps {
        checkout scm
        sh '''
          python -m pip install --upgrade pip
          pip install safety bandit
        '''
        // Scan des dépendances
        sh 'safety check || echo "Security vulnerabilities found in dependencies"'
        // Scan du code
        sh 'bandit -r . -f json -o bandit-report.json || echo "Security issues found in code"'
      }
      post {
        always {
          archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
        }
      }
    }

    // Étape 6: Déploiement Staging (simulé)
    stage('Deploy to Staging') {
      when { branch 'develop' }
      agent any
      steps {
        echo "🚀 Déploiement simulé sur staging"
        echo "Image: ${APP_NAME}:${BRANCH_NAME}-${BUILD_NUMBER}"
        echo "Package: dist/*.whl"
      }
    }

    // Étape 7: Validation manuelle
    stage('Approbation Production') {
      when { branch 'develop' }
      agent none
      steps {
        input message: "Déployer en production?", ok: "Confirmer"
      }
    }

    // Étape 8: Déploiement Production (simulé)
    stage('Deploy to Production') {
      when { 
        anyOf { 
          branch 'main'
          expression { return true } // Toujours exécuté après approbation
        }
      }
      agent any
      steps {
        echo "🚀 DÉPLOIEMENT PRODUCTION SIMULÉ"
        echo "Version: ${APP_NAME}:${BRANCH_NAME}-${BUILD_NUMBER}"
        echo "Artefact: dist/*.whl"
      }
    }
  }

  post {
    always {
      echo "✅ Pipeline terminée"
      cleanWs()
    }
    success {
      echo "👉 SUCCÈS: ${env.BUILD_URL}"
      emailext body: "Build Python réussi!\n\nDétails: ${env.BUILD_URL}\nArtefacts: dist/*",
              subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
              to: "${TEAM_EMAIL}"
    }
    failure {
      echo "❌ ÉCHEC: Veuillez vérifier les logs"
      emailext body: "Échec du pipeline Python!\n\nConsulter les logs: ${env.BUILD_URL}",
              subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
              to: "${TEAM_EMAIL}"
    }
    unstable {
      echo "⚠️ Des tests sont instables"
      emailext body: "Pipeline Python instable (tests échoués)\n\nDétails: ${env.BUILD_URL}",
              subject: "UNSTABLE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
              to: "${TEAM_EMAIL}"
    }
  }
}