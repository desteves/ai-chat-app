# AI Chat Application Demo

AI Chat application that uses OpenAI + Pinecone. Monitored by New Relic. Deployed by Pulumi on AWS.

## Pre-requisites

- New Relic license key
- Pinecone API Key
- Open API Key

## Deploy to AWS with Pulumi

Additional requirements:

- AWS Account + [local credentials configured](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html)
- [Pulumi Cloud account](https://app.pulumi.com/) + [Pulumi CLI](https://www.pulumi.com/docs/install/)

### 1. Store app secrets in Pulumi ESC

```bash
# store app secrets
E=my-cool-chat-app-env
pulumi env init $E --non-interactive
pulumi env set  $E environmentVariables.NEW_RELIC_LICENSE_KEY 123ABC --secret 
pulumi env set  $E environmentVariables.NRIA_LICENSE_KEY 123ABC --secret 
pulumi env set  $E environmentVariables.OPENAI_API_KEY 123ABC --secret 
pulumi env set  $E environmentVariables.PINECONE_API_KEY 123ABC --secret 
```

### 2. Store infra secrets in Pulumi ESC

Additional prerequisites:

- Create a [Pulumi Cloud access token](https://www.pulumi.com/docs/pulumi-cloud/access-management/access-tokens/) for the EC2 Instance to access your app secrets Environment. If you're on a paid tier, you can create a custom team with only read access to the app secrets environment to adhere to the principle of least privilige.🔐
- Gather your [New Relic access details](https://www.pulumi.com/registry/packages/newrelic/installation-configuration/#configuring-credentials).
- Create a new [Pinecone key](https://www.pulumi.com/registry/packages/pinecone/installation-configuration/#configuration). Alternatively, you can re-use the same key for the app by importing the app secrets. The latter approach is demostrated below.
- Get a [Docker PAT](https://docs.docker.com/security/for-developers/access-tokens/) to push the docker images to your own Dockerhub registry

```bash
# store infra secrets
C=my-cool-chat-app-provider-creds
pulumi env init $C --non-interactive
pulumi env edit $C
# // to the very top of the ESC Environment add the following:
# 
# imports:
#  - my-cool-chat-app-env
# 
# // save the changes and exit.

# reference the existing Pinecone key
pulumi env set $C pulumiConfig.pinecone:APIKey \${environmentVariables.PINECONE_API_KEY}

# Enable the EC2 to access app secrets
pulumi env set $C environmentVariables.PULUMI_TEAM_TOKEN_EC2_ESC pul-123ABC --secret

# New Relic
pulumi env set $C pulumiConfig.newrelic:accountId 123456
pulumi env set $C pulumiConfig.newrelic:apiKey 123ABC --secret
pulumi env set $C pulumiConfig.newrelic:adminApiKey 123ABC --secret

# Docker
pulumi env set $C pulumiConfig.DOCKER_PAT 123ABC --secret
pulumi env set $C pulumiConfig.DOCKER_USR nullstring ## 🚨🚨🚨 replace with YOUR handle

# Add the infra secrets environment to pulumi
pulumi config env add $C --stack dev --yes
```

### 3. Deploy everything 🚀

```bash
# start up a venv and install deps
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Additional AWS configurations
# https://www.pulumi.com/registry/packages/aws-native/installation-configuration/
# the option shown here uses your ~/.aws/credentials profile name
# aws sso --profile work
pulumi config set aws:profile work ## 🚨🚨🚨 replace with YOUR profile name
pulumi config set aws:region us-west-2
# option to enable auth via EC2 Instance Metadata
pulumi config set aws:skipMetadataApiCheck false

###
### ARE YOU READY!?
# Time to Deploy 
pulumi up --stack dev --yes
# Ta - Da! ✨🎉
```

Learn how to [configure AWS OIDC with Pulumi ESC](https://www.pulumi.com/docs/esc/providers/aws-login/) for an even more secure configuration.

## Run Locally via Docker

Additional requirements:

- Docker
- A Pinecone index named `games` in the `default` namespace that needs to use the `text-embedding-ada-002` model.
- Update the `dashboard.json` accountIds array to include YOUR New Relic account id.
- Import the `dashboard.json` to your New Relic account.
- Rename [app/.env.example](./app/.env.example) to `app/.env` and update the variables as shown in the [docker-compose.yml](./app/docker-compose.yml) comments.

```bash
cd app
docker compose up -d
```

## Acknowledgements

This repo stems from existing work by @harrykimpel

- [Node Chat Service](https://github.com/harrykimpel/node-chat-service)
- [Chat Front-End](https://github.com/harrykimpel/python-flask-openai/tree/main/chat-frontend)
