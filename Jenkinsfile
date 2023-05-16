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
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip3 install -r requirements.txt'
                }
         }
        
    }
}
