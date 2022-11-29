import os

from prefect import flow, task
import prefect


@task(name="Load", retries=3, retry_delay_seconds=30)
def say_something(a: str):
    logger = prefect.get_run_logger()
    logger.info(msg=a)
    return


@flow
def print_flow():
    say_something(os.getenv("STAGPROD"))
