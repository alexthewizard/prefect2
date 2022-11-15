from print_flow import print_flow
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

github_block = GitHub.load("alex-repo")

deployment = Deployment.build_from_flow(
    flow=print_flow,
    name="print-simple",
    work_queue_name="default",
    storage=github_block
)

deployment.apply()
