pipeline {
    agent any 
    stages {
        stage('git repo & clean') {
            steps {
                sh "rm -r Blogs"
                sh "git clone https://github.com/nidhipanchal23/Blogs.git"
                // sh "mvn clean -f Blogs"
            }  
        }
         stage('Install Dependencies') {
            steps {
//                sh 'apt-get update && apt-get install -y python3-pip'
                sh 'pip3 install pipenv'

                // Install project dependencies
                sh 'pipenv install --deploy --system'
                }
         }
    }
}
