FROM prefecthq/prefect:2.6.5-python3.8

COPY requirements.txt .

ARG PIP_INDEX_URL

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && python -m pip cache purge