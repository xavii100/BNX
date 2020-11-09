  pipeline {
    agent { label 'python36' }
    options { timeout(time: 20, unit: 'MINUTES') }
    stages {
      stage('Initialise') {
        steps {
          stepInitialise()
          stepPythonConfigure()
        }
      }
      stage('Python Build & Test') {
        steps {
          sh """
            python -m venv .env
            source ./.env/bin/activate
            python -m pip install -r requirements.txt
            python -m pip install pytest pytest-cov coverage
            
            if [ -d 'tests' ]; then          
              python -m pytest --cov-report xml --cov=. --junitxml=test_results.xml ./tests
            else
              python -m pytest
            fi
            """
        }
      }
      stage('Sonar Analysis') {
        steps {
          stepPythonSonarAnalysis()
        }
      }
      stage('Build container image') {
        steps {
          stepContainerImageBuild()
        }
      }
      stage('Build ECS deployment image') {
        when { expression { return env.LS_GIT_BRANCH ==~ "master|feature.*" } }
        steps {
          stepEcsDeploymentImageBuild()
        }
      }
      stage('Test Deployment') {
        when { expression { return env.LS_GIT_BRANCH ==~ "master|feature.*" } }
        steps {
          stepEcsDeploy()
        }
      }
      stage('Publish to uDeploy') {
        when { expression { return env.LS_GIT_BRANCH ==~ "feature.*" } }
        steps {
          stepEcsUdeployPublish()
        }
      }
    }
    post {
      always {
        script{
        	// clean up any objects created by this pipeline run
          // sh "oc delete all -l lightspeed-build-id=${env.LS_BUILD_ID}"

          if (env.LS_GIT_BUILDING_FROM_TAG.equals("true") && env.LS_VERSION_MODE.equals("branch"))
            return;
          currentBuild.result = currentBuild.result ?: 'SUCCESS'
          if (globalLoki.isEnabled()) {
            internalLokiFinalize()
          }
          if (currentBuild.result == 'SUCCESS') {
            internalBlackDuck.uploadWorkspaceArchiveIfNeeded()
          }

          notifyBitbucket(
            commitSha1: "${env.GIT_COMMIT}",
            stashServerBaseUrl: "${env.LS_BITBUCKET_URL}",
            includeBuildNumberInKey: false
          )
        }
      }
    }
  }
