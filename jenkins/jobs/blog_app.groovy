folder('Blogs') {

    displayName('Blogs')

    description('Automatically created project folder')

}


pipelineJob('Blogs/blog_app') {


    description(
        'Generated automatically by DevOps Platform'
    )


    definition {


        cpsScm {


            scm {


                git {


                    remote {


                        url('https://github.com/akashnegi62/devops-platform.git')


                        credentials('github-token')


                    }


                    branch('main')


                }


            }


            scriptPath('generated/jenkinsfiles/blog_app/Jenkinsfile')


        }


    }


}