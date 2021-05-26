#!groovy
pipeline {
    environment {
        VERSION = ''
        HELM_USERNAME='crosslang'
        HELM_PASSWORD='isthebest'
        BUILD_VERSION = sh(script: "echo $BUILD_ID-$BRANCH_NAME \\[`date '+%Y-%m-%d %H:%M'`\\]", returnStdout: true).trim()
    }

    agent { label 'master' }

    stages {
        stage('Build Docker images') {
            steps {
                dir('backend'){
                    script {
                        docker.withRegistry("https://docker.crosslang.com", "docker-crosslang-com") {
                            def customImage = docker.build("occam_doc_manager/django:${env.BRANCH_NAME}-${env.BUILD_ID}", "-f Dockerfile --build-arg APP_VERSION=\"${env.BUILD_VERSION}\" .")
                            customImage.push()
                            customImage.push("${env.BRANCH_NAME}-latest")
                        }
                    }
                }
                dir('backend/nginx'){
                    script {
                        docker.withRegistry("https://docker.crosslang.com", "docker-crosslang-com") {
                            def customImage = docker.build("occam_doc_manager/django_nginx:${env.BRANCH_NAME}-${env.BUILD_ID}", "-f Dockerfile .")
                            customImage.push()
                            customImage.push("${env.BRANCH_NAME}-latest")
                        }
                    }
                }
                dir('frontend'){
                    script {
                        docker.withRegistry("https://docker.crosslang.com", "docker-crosslang-com") {
                            def customImage = docker.build("occam_doc_manager/react:${env.BRANCH_NAME}-${env.BUILD_ID}", "-f Dockerfile --build-arg APP_VERSION=\"${env.BUILD_VERSION}\" .")
                            customImage.push()
                            customImage.push("${env.BRANCH_NAME}-latest")
                        }
                    }
                }
            }
        }
//         stage('Deploy Helm Chart') {
//             steps {
//                 dir('deploy/helm'){
//                     sh './kompose.sh'
//                 }
//             }
//         }
    }
}