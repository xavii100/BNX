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
          script {
            Map overrides = [:]
            final sonarRunner = "/tmp/sonar-scanner-4.2.0.1873/bin/sonar-scanner"
            final sonarRunnerUrl = "${env.LS_ARTIFACTORY_SERVER_URL}/generic-icg-dev-local/msst-infra-171981/sonar/sonar-scanner-cli-4.2.0.1873.zip"

            withCredentials([usernameColonPassword(credentialsId: 'citi-ear', variable: 'LS_ARTIFACTORY_CREDS')]) {
              echo "[SonarQube] Initialize Sonar Runner..."
              sh script: """
              if [ ! -f "$sonarRunner" ]; then
                  cd /tmp
                  curl -fsSL -u${LS_ARTIFACTORY_CREDS} "$sonarRunnerUrl" > sonar.zip
                  unzip sonar.zip -d /tmp && rm sonar.zip
                  chmod +x "$sonarRunner"
              fi
              """
            }

            withCredentials([string(credentialsId: 'msst-sonarqube', variable: 'LS_SONAR_TOKEN')]) {
              Map values = [:]
              values["sonar.host.url"] = "${env.LS_SONAR_SERVER}"
              values["sonar.login"] = "${LS_SONAR_TOKEN}"
              values["sonar.projectKey"] = "${env.LS_SONAR_PROJECT_KEY}"
              values["sonar.projectName"] = "${env.LS_SONAR_PROJECT_NAME}"
              values["sonar.branch.name"] = "${env.LS_SONAR_BRANCH_NAME}"
              values["sonar.sources"] = "."
              values["sonar.exclusions"] = "tests/**,**/log.*,**/properties.*,**/properties_db.*,**/properties_exc.*,**/properties_log.*,**/setup.*,**/__init__.*,**/custom_messages.*,**/custom_config.*"
              values["sonar.tests"] = "tests"
              values["python.xunit.reportPath"] = "test*.xml"
              values["sonar.python.coverage.reportPaths"] = "*coverage.xml"
              values["sonar.sourceEncoding"] = "utf-8"
              values["sonar.verbose"] = "false"
              values << overrides

              sh "$sonarRunner ${values.collect { k, v -> "\"-D$k=$v\"" }.join(' ')}"
            }
          }
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
