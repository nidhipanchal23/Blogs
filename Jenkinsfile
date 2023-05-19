pipeline {
    agent any
    stages {
        stage('git repo & clean') {
            steps {
//                 script {
//                     // Check if directory exists before removing it
//                     if (fileExists('Blogs')) {
                        sh 'rm -r Blogs'
//                     }
//                 }
                sh "git clone https://github.com/nidhipanchal23/Blogs.git"
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
                sh 'export RUN_MAIN=true && export DJANGO_SETTINGS_MODULE=blog.settings'
                sh '. venv/bin/activate && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py collectstatic --noinput'
//                 sh ' /var/lib/jenkins/workspace/hubstaff4/venv/bin/gunicorn blog.wsgi:application --bind 0.0.0.0:8000'
                }
         }
        
    }
}
