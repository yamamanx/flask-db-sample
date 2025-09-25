#!/bin/bash

PROFILE=yamamugi-ninjya
ACCOUNT_ID=$(aws sts get-caller-identity --profile $PROFILE --query Account --output text)
REGION=us-east-1
REPO_NAME=selenium-lambda-test

# ECRリポジトリ作成
aws ecr create-repository --repository-name $REPO_NAME --region $REGION --profile $PROFILE || true

# ログイン
aws ecr get-login-password --region $REGION --profile $PROFILE | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# ビルドとプッシュ
docker build -t $REPO_NAME .
docker tag $REPO_NAME:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest