pipeline {
  agent any  // Utilise votre agent Jenkins Alpine par défaut
  
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
    timeout(time: 20, unit: 'MINUTES')  // Augmenté car installation des outils
    timestamps()
  }

  environment {
    APP_NAME = "demo-app"
    BRANCH_NAME = env.BRANCH_NAME.replaceAll('/', '-')
    TEAM_EMAIL = 'koussougboss@gmail.com, huguesblakime@gmail.com'
    PYTHONPATH = "${WORKSPACE}"
  }

  stages {
    // Étape 1: Installation des outils
    stage('Setup Environment') {
      steps {
        checkout scm
        sh '''
          # Installation de Python et des outils système
          apk add --no-cache python3 py3-pip python3-dev gcc musl-dev libffi-dev
          python3 -m ensurepip
          
          # Création d'un lien symbolique pour python
          ln -sf python3 /usr/bin/python
          
          # Création de l'environnement virtuel
          python -m venv venv
          
          # Activation de l'environnement virtuel et installation des packages
          . venv/bin/activate
          
          # Mise à jour de pip dans le venv
          pip install --upgrade pip
          
          # Installation des dépendances du projet
          pip install -r dev-requirements.txt
          
          # Installation des outils de qualité de code
          pip install flake8 black isort mypy pytest pytest-cov pytest-xvfb safety bandit build wheel
          
          # Vérification que tout est bien installé
          echo "✅ Environnement virtuel créé et configuré"
          which python
          which pip
          python --version
        '''
      }
    }

    // Étape 2: Qualité de code et tests
    stage('Quality & Test') {
      parallel {
        stage('Code Quality') {
          steps {
            sh '''
              # Activation de l'environnement virtuel
              . venv/bin/activate
              
              echo "🔍 Vérification du formatage avec Black..."
              black --check . || echo "❌ Code formatting issues found"
              
              echo "🔍 Vérification des imports avec isort..."
              isort --check-only . || echo "❌ Import sorting issues found"
              
              echo "🔍 Analyse avec flake8..."
              flake8 . || echo "❌ Linting issues found"
              
              echo "🔍 Vérification des types avec mypy..."
              mypy . || echo "❌ Type checking issues found"
            '''
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
          steps {
            sh '''
              # Activation de l'environnement virtuel
              . venv/bin/activate
              
              echo "🧪 Exécution des tests unitaires..."
              pytest --cov=. --cov-report=xml --cov-report=html --junitxml=test-results.xml
            '''
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
      steps {
        sh '''
          # Activation de l'environnement virtuel
          . venv/bin/activate
          
          echo "📦 Construction du package Python..."
          python -m build
        '''
        archiveArtifacts artifacts: 'dist/*', fingerprint: true
      }
    }

    // Étape 4: Security Scan
    stage('Security Scan') {
      when { branch 'develop' }
      steps {
        sh '''
          # Activation de l'environnement virtuel
          . venv/bin/activate
          
          echo "🔒 Scan des vulnérabilités des dépendances..."
          safety check || echo "❌ Security vulnerabilities found in dependencies"
          
          echo "🔒 Scan de sécurité du code..."
          bandit -r . -f json -o bandit-report.json || echo "❌ Security issues found in code"
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
        }
      }
    }

    // Étape 5: Déploiement Staging (simulé)
    stage('Deploy to Staging') {
      when { branch 'develop' }
      steps {
        echo "🚀 Déploiement simulé sur staging"
        echo "Package: dist/*.whl"
      }
    }

    // Étape 6: Validation manuelle
    stage('Approbation Production') {
      when { branch 'develop' }
      steps {
        input message: "Déployer en production?", ok: "Confirmer"
      }
    }

    // Étape 7: Déploiement Production (simulé)
    stage('Deploy to Production') {
      when { 
        anyOf { 
          branch 'main'
          expression { return true }
        }
      }
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