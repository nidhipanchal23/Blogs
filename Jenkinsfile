pipeline {
    agent {
        docker { image 'python:3' } 
    }
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
                sh 'pip install -r requirements.txt'
                }
         }
    }
}
