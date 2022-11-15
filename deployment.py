from print_flow import print_flow
from prefect.deployments import Deployment

deployment = Deployment.build_from_flow(
    flow=print_flow,
    name="print-simple",
    work_queue_name="default",
)

deployment.apply()
