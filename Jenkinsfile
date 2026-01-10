pipeline{
    agent any

    stages{
        stage('Checkout Code'){
            steps{
                echo "Cloning the Repository"
                
                try{
                    checkout scm
                    echo "Repository cloned Successfully"
                } catch(err){
                    echo "Repository clone failed"
                    echo "Error message : ${err}"

                    currentBuild.result = 'FAILURE'
                    error("Stopping pipeline due to checkout failure")
                }
            }
        }

        stage('Setting Up python'){
            steps {
                echo "Setting up the python Environment and Installations"

                try{
                    sh '''
                    set -e
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate

                    echo "⬆️ Upgrading pip"
                    pip install --upgrade pip

                    echo "📦 Installing required Python packages"
                    pip install selenium pytest pytest-html
                    '''

                    echo "Python environment setup completed"
                } catch(err) {
                    echo 'Python environment setup FAILED'
                    echo "Failure reason: ${err}"

                    currentBuild.result = 'FAILURE'
                    error('Stopping pipeline due to Python package installation failure')
                }
            }
        }

        stage('Run Selenium Tests'){
            steps{
                script {
                    echo 'Running the Selennium tests'

                    try{
                        sh '''
                        set -e
                        . venv/bin/activate

                        echo "▶️ Starting pytest"
                        pytest pythonSel/test_e2eTestFramework.py \
                            --browser_name chrome \
                            --html=reports/report.html \
                            --self-contained-html
                        '''

                        echo '✅ Selenium tests completed successfully'
                    } catch(err){
                        echo 'Selenium tests FAILED'
                        echo "Failure reason: ${err}"

                        currentBuild.result = 'FAILURE'
                        error('Stopping pipeline due to Selenium test failure')
                    }
                }
            }
        }
    }
}