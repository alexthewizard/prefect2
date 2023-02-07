function aws_account {
    echo $(aws sts get-caller-identity --output text --query "Account" )
}

function aws_region {
    if [ $# -eq 1 ]; then
            aws configure set region "$1"
        fi

    echo ${AWS_DEFAULT_REGION:-$(aws configure get region)}
}

function aws_ecr_repo {
    echo $(aws_account).dkr.ecr.$(aws_region).amazonaws.com/$1
}

function aws_codeartifact_pip_login {
    aws codeartifact login --tool pip --repository pypi --domain landtech-data --domain-owner 825489050785
}
