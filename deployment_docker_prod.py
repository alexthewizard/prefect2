from print_flow import print_flow
from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer, DockerRegistry
from prefect.filesystems import GitHub
import boto3
import base64


client = boto3.client('ecr')

token = client.get_authorization_token()['authorizationData'][0]['authorizationToken']
token = base64.b64decode(token).decode('utf-8')
username, password = token.split(':')

github_block = GitHub(
    repository="https://github.com/alexthewizard/prefect2.git",
)
github_block.save('alex-repo', overwrite=True)

docker_registry = DockerRegistry(
    username=username,
    password=password,
    registry_url='845587943863.dkr.ecr.eu-west-1.amazonaws.com'
)
docker_registry.save('data-hub-registry', overwrite=True)

docker_container_block = DockerContainer(
    image='845587943863.dkr.ecr.eu-west-1.amazonaws.com/data-hub-constraints-prefect2',
    docker_registry=docker_registry,
    image_pull_policy='ALWAYS'
)

deployment = Deployment.build_from_flow(
    flow=print_flow,
    name="print-simple-docker-prod",
    work_queue_name="default",
    storage=github_block,
    infrastructure=docker_container_block,
    infra_overrides={"env.STAGPROD": "prod"}
)

deployment.apply()
