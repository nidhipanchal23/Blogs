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
                sh '/var/lib/jenkins/workspace/hubstaff4/venv/bin/pip3 install -r requirements.txt'
                }
         }
        stage('run') {
            steps {
                sh 'export PGPASSWORD=ct##123456 && psql -h 127.0.0.1 -p 5432 -U postgres -d blogs -c "SELECT 1;"'
                sh '. venv/bin/activate && python3 manage.py makemigration && python3 manage.py migrate'
                sh 'python3 manage.py runserver'
                }
         }
        
    }
}
