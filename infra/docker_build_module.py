"""_summary_
"""
import pulumi
import pulumi_docker_build as docker_build

username = pulumi.Config().require("DOCKER_USR")

def build_push_images():
    """_summary_
    """
    # Build and push the Docker images
    image_web = docker_build.Image(
      'ai-chat-demo-web',
      context=docker_build.BuildContextArgs(
        location='../app/web',
      ),
      tags=[f'docker.io/{username}/ai-chat-demo-web:latest'],
      push=True,
      registries=[docker_build.RegistryArgs(
        address='docker.io',
        username=username,
        password=pulumi.Config().require_secret('DOCKER_PAT'),
      )]
    )
    image_api = docker_build.Image(
      'ai-chat-demo-api',
      context=docker_build.BuildContextArgs(
        location='../app/api',
      ),
      tags=[f'docker.io/{username}/ai-chat-demo-api:latest'],
      push=True,
      registries=[docker_build.RegistryArgs(
        address='docker.io',
        username=username,
        password=pulumi.Config().require_secret('DOCKER_PAT'),
      )]
    )
