// pipeline{
//     agent any

//     stages{
//         stage('Checkout Code'){
//             steps{
//                 echo "Cloning the Repository"
                
//                 try{
//                     checkout scm
//                     echo "Repository cloned Successfully"
//                 } catch(err){
//                     echo "Repository clone failed"
//                     echo "Error message : ${err}"

//                     currentBuild.result = 'FAILURE'
//                     error("Stopping pipeline due to checkout failure")
//                 }
//             }
//         }

//         stage('Setting Up python'){
//             steps {
//                 echo "Setting up the python Environment and Installations"

//                 try{
//                     sh '''
//                     set -e
//                     python3 --version
//                     python3 -m venv venv
//                     . venv/bin/activate

//                     echo "⬆️ Upgrading pip"
//                     pip install --upgrade pip

//                     echo "📦 Installing required Python packages"
//                     pip install selenium pytest pytest-html
//                     '''

//                     echo "Python environment setup completed"
//                 } catch(err) {
//                     echo 'Python environment setup FAILED'
//                     echo "Failure reason: ${err}"

//                     currentBuild.result = 'FAILURE'
//                     error('Stopping pipeline due to Python package installation failure')
//                 }
//             }
//         }

//         stage('Run Selenium Tests'){
//             steps{
//                 script {
//                     echo 'Running the Selennium tests'

//                     try{
//                         sh '''
//                         set -e
//                         . venv/bin/activate

//                         echo "▶️ Starting pytest"
//                         pytest pythonSel/test_e2eTestFramework.py \
//                             --browser_name chrome \
//                             --html=reports/report.html \
//                             --self-contained-html
//                         '''

//                         echo '✅ Selenium tests completed successfully'
//                     } catch(err){
//                         echo 'Selenium tests FAILED'
//                         echo "Failure reason: ${err}"

//                         currentBuild.result = 'FAILURE'
//                         error('Stopping pipeline due to Selenium test failure')
//                     }
//                 }
//             }
//         }
//     }
// }

// pipeline {
//     agent any

//     stages {
//         stage('Checkout Code') {
//             steps {
//                 script {
//                     try {
//                         echo "Cloning the Repository"
//                         checkout scm
//                         echo "Repository cloned Successfully"
//                     } catch (err) {
//                         echo "Repository clone failed"
//                         echo "Error message: ${err}"
//                         currentBuild.result = 'FAILURE'
//                         error("Stopping pipeline due to checkout failure")
//                     }
//                 }
//             }
//         }

//         stage('Setting Up Python') {
//             steps {
//                 script {
//                     try {
//                         echo "Setting up the Python environment"

//                         sh '''
//                         set -e
//                         python3 --version
//                         python3 -m venv venv
//                         . venv/bin/activate

//                         echo "⬆️ Upgrading pip"
//                         pip install --upgrade pip

//                         echo "📦 Installing required Python packages"
//                         pip install selenium pytest pytest-html
//                         '''

//                         echo "Python environment setup completed"
//                     } catch (err) {
//                         echo 'Python environment setup FAILED'
//                         echo "Failure reason: ${err}"
//                         currentBuild.result = 'FAILURE'
//                         error('Stopping pipeline due to Python package installation failure')
//                     }
//                 }
//             }
//         }

//         stage('Run Selenium Tests') {
//             steps {
//                 script {
//                     try {
//                         echo 'Running the Selenium tests'

//                         sh '''
//                         set -e
//                         . venv/bin/activate

//                         echo "▶️ Starting pytest"
//                         pytest pythonSel/test_e2eTestFramework.py \
//                             --browser_name chrome \
//                             --html=reports/report.html \
//                             --self-contained-html
//                         '''

//                         echo '✅ Selenium tests completed successfully'
//                     } catch (err) {
//                         echo 'Selenium tests FAILED'
//                         echo "Failure reason: ${err}"
//                         currentBuild.result = 'FAILURE'
//                         error('Stopping pipeline due to Selenium test failure')
//                     }
//                 }
//             }
//         }
//     }
// }


pipeline {
    agent any

     options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMAGE_NAME = "selenium-test-image"
        CONTAINER_NAME = "selenium-test-container-${BUILD_NUMBER}"
        REPORT_BASE_PATH = "/opt/selenium-test-reports"
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    try {
                        echo "Cloning the Repository"
                        checkout scm
                        echo "Repository cloned Successfully"
                    } catch (err) {
                        echo "Repository clone failed"
                        echo "Error message: ${err}"
                        currentBuild.result = 'FAILURE'
                        error("Stopping pipeline due to checkout failure")
                    }
                }
            }
        }

        stage('Docker Image Creation'){
            steps{
                script{
                    echo "Creating the Docker Image for Test !"

                    try{
                        sh '''
                        set -e

                        echo "Building Docker Image"
                        docker build -t $IMAGE_NAME .

                        echo "Image created successfully"
                        '''
                    } catch(err){
                        echo "Docker Image creation FAILED"
                        echo "Error details : ${err}"
                        currentBuild.result = 'FAILURE'
                        error("Stopping pipeline due to Docker Image creation failure")
                    }
                }
            }
        }

        stage('Docker Container Creation'){
            steps{
                script{
                    echo "Docker Container creation & running Tests"

                    try{
                        sh '''
                        echo "Running Docker container"
                        set -e
                        mkdir -p reports

                        docker run --name $CONTAINER_NAME \
                        -v $WORKSPACE/reports:/home/seluser/project/reports \
                        $IMAGE_NAME
                        '''

                        echo "Tests are Completed Successfully"
                    } catch(err){
                        echo "Docker container execution FAILED"
                        echo "Error details: ${err}"
                        currentBuild.result = 'FAILURE'
                        error("Stopping pipeline due to test execution failure")
                    }
                }
            }
        }

        stage('Building GmailHTML file'){
            steps{
                script{

                    sh '''
                    cd pythonSel
                    python3 generate_mail_html.py
                    '''
                }
            }
        }
    }

    post {
        always {
            script{
                def ts = sh(script: "date '+%Y-%m-%d_%H-%M-%S'", returnStdout: true).trim()
                def finalPath = "${REPORT_BASE_PATH}/${ts}"
                def finalPathForEmail = "${finalpath}/mail_report.html"

                sh """
                mkdir -p ${finalPath}
                cp -r reports/* ${finalPath}/ || true
                """

                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            }

            echo "Files Moved to local succefully"

            sh '''
            docker rm -f $CONTAINER_NAME || true
            docker rmi -f $IMAGE_NAME || true
            '''
        }

        success {
            echo "🎉 Pipeline completed successfully"
            script{
                echo "Sending Automation Test Report Mail"

            def mailBody = readFile(finalPathForEmail)

            emailext(
                subject: "✅ Automation Test Report - SUCCESS",
                body: mailBody,
                mimeType: 'text/html',
                to: "prasanna@codifi.in"
            )
            }
        }

        failure {
            echo "🚨 Pipeline failed – reports & screenshots saved"

            script{
                emailext(
                subject: "🚨 Automation Test FAILED",
                body: """
                Tests failed or report generation failed.
                Please check Jenkins console and reports.
                """,
                to: "prasanna@codifi.in"
                )
            }
        }
    }
}


