pipeline {
    agent any
    stages {
        stage('git repo & clean') {
            steps {
                sh "git clone https://github.com/nidhipanchal23/Blogs.git"
                sh "mvn clean -f Blogs"
            }
        }
    }
}
