source ./aws_functions.sh

ECR_REGISTRY=$(aws_ecr_repo | sed 's:/*$::')
FLOW_IMAGE_NAME="data-hub-constraints-prefect2"

CODEARTIFACT_DOMAIN="landtech-data"
CODEARTIFACT_REPO="pypi"
AWS_ACCOUNT_ID="825489050785"

if [ -z "$AWS_DEFAULT_REGION" ]; then
  export AWS_DEFAULT_REGION=$(aws configure get region)
fi
# Log in to ECR, make sure flow repo exists and set or update lifecycle policy
aws ecr get-login-password | docker login --username AWS --password-stdin "$ECR_REGISTRY"
aws ecr create-repository --repository-name "${FLOW_IMAGE_NAME}" || true

CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token --domain ${CODEARTIFACT_DOMAIN} --domain-owner ${AWS_ACCOUNT_ID} --query authorizationToken --output text)

PIP_INDEX_URL="https://aws:${CODEARTIFACT_AUTH_TOKEN}@${CODEARTIFACT_DOMAIN}-${AWS_ACCOUNT_ID}.d.codeartifact.${AWS_DEFAULT_REGION}.amazonaws.com/pypi/${CODEARTIFACT_REPO}/simple/"
echo "$PIP_INDEX_URL"
docker build -t ${ECR_REGISTRY}/${FLOW_IMAGE_NAME}:latest . --build-arg PIP_INDEX_URL=$PIP_INDEX_URL
docker push ${ECR_REGISTRY}/${FLOW_IMAGE_NAME}:latest
