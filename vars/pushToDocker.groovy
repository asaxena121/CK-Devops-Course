def call(Map config = [:]) {
    def imageName = config.image ?: error("Missing parameter: 'image'")
    def imageTag  = config.tag ?: 'latest'
    def credentialsId = config.credentialsId ?: error("Missing parameter: 'credentialsId'")

    withCredentials([usernamePassword(credentialsId: credentialsId, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
        sh """
            echo "Logging in to Docker Hub..."
            echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin

            echo "Tagging image ${imageName}:${imageTag}..."
            docker tag ${imageName}:${imageTag} \$DOCKER_USER/${imageName}:${imageTag}

            echo "Pushing image to Docker Hub..."
            docker push \$DOCKER_USER/${imageName}:${imageTag}

            echo "Docker image pushed successfully."
        """
    }
}
