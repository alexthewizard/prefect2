FROM prefecthq/prefect:2.6.5-python3.8

ENTRYPOINT [ "prefect", "agent", "start", "-q", "default" ]