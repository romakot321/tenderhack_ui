#!groovy


def agentLabel
def project_name = 'diana-bot_' + env.BRANCH_NAME
if (env.BRANCH_NAME == "release"){
    agentLabel = "production"
} else {
    agentLabel = "phys"
}
pipeline {
    agent { label agentLabel }
    stages {
        stage("Build and up") {
            steps {
                sh "cp /home/jenkins/weights/diana-bot.env .env"
                sh "docker-compose -f docker-compose.prod.yml up -d --build --remove-orphans || docker compose -f docker-compose.prod.yml up -d --build --remove-orphans"
            }
        }
    }
}
