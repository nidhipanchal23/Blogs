pipeline {
    agent any
    stages {
        stage('git repo') {
            steps {
                sh "git clone https://github.com/nidhipanchal23/Blogs.git"
            }
        }
        stage('install') {
            steps {
                sh "mvn install -f Blogs"
            }
        }
        stage('test') {
            steps {
                sh "mvn test -f Blogs"
            }
        }
        stage('package') {
            steps {
                sh "mvn package -f Blogs"
            }
        }
    }
}
