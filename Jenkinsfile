pipeline {
    agent any
    stages {
         stage('git repo') {
            steps {
                sh "git clone https://github.com/nidhipanchal23/Blogs.git"
                }
         stage('run') {
            steps {
                sh "python manage.py runserver"
                }
            }
        }
    }
}
