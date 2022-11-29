from print_flow import print_flow
from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from prefect.filesystems import GitHub

github_block = GitHub.load("alex-repo")
docker_container_block = DockerContainer.load("alex-docker")

deployment = Deployment.build_from_flow(
    flow=print_flow,
    name="print-simple-docker-prod",
    work_queue_name="default",
    storage=github_block,
    infrastructure=docker_container_block,
    infra_overrides={"env.STAGPROD": "prod"}
)

deployment.apply()
