from print_flow import print_flow
from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from prefect.filesystems import GitHub

github_block = GitHub(
    repository="https://github.com/alexthewizard/prefect2.git",
)
github_block.save('alex-repo', overwrite=True)
docker_container_block = DockerContainer(
    env={
        "PREFECT_API_URL": "http://host.docker.internal:4200/api"
    }
)
docker_container_block.save('docker-container', overwrite=True)

deployment = Deployment.build_from_flow(
    flow=print_flow,
    name="print-simple-docker-staging",
    work_queue_name="default",
    storage=github_block,
    infrastructure=docker_container_block,
    infra_overrides={"env.STAGPROD": "staging"}
)

deployment.apply()
