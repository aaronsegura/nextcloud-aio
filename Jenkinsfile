pipeline {
  agent any

  stages {
    stage('Install Package') {
      steps {
        withPythonEnv('python3') {
          sh 'python3 -mpip install .'
        }
      }
    }

    stage('Run Tests') {
      parallel {
        stage('flake8 check') {
          agent {
            docker {
              image 'pipelinecomponents/flake8'
              args '-v $PWD:/data'
            }
          }
          steps {
            sh 'flake8 --exclude .git,__pycache__,node_modules,.pyenv* --count --statistics . || true'
          }
        }
        stage('pydocstyle check') {
          agent {
            dockerfile {
              dir '.jenkins'
              filename 'Dockerfile-pydocstyle'
            }
          }
          steps {
            sh 'pydocstyle --convention=pep257 --count nextcloud_aio || true'
          }
        }
        stage('unit tests') {
          steps {
            withPythonEnv('python3') {
              dir('tests') {
                sh 'python3 -munittest'
              }
            }
          }
        }
      } // parallel
    } // Run Tests
  } // stages
} // pipeline