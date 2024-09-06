# AI Chat Application Demo

Chat application that uses OpenAI + Pinecone. Monitored by New Relic. Deployed with Pulumi on AWS.

## Pre-requisites

- New Relic license key
- Pinecone API Key
- Open API Key

## Deploy to AWS with Pulumi

Additional requirements:

- AWS Account + credentials
- Pulumi Cloud account

```bash
cd infra

# log in 
pulumi login

# configure the environment once
E=my-cool-chat-app-env
pulumi env init $E --non-interactive
pulumi env set  $E environmentVariables.NEW_RELIC_LICENSE_KEY 123ABC --secret 
pulumi env set  $E environmentVariables.NRIA_LICENSE_KEY 123ABC --secret 
pulumi env set  $E environmentVariables.OPENAI_API_KEY 123ABC --secret 
pulumi env set  $E environmentVariables.PINECONE_API_KEY 123ABC --secret 

# consume in N places
pulumi env open $E --format dotenv > ../app/.env

# start up a venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pulumi stack init dev

# pulumi needs credentials to your NR, Pinecone and AWS accounts
C=my-cool-chat-app-provider-creds
pulumi env init $C --non-interactive

# for AWS
# https://www.pulumi.com/registry/packages/aws-native/installation-configuration/
# the option shown here uses your ~/.aws/credentials profile name
# aws sso --profile work
pulumi config set aws:profile work
pulumi config set aws:region us-west-2
# option to enable auth via EC2 Instance Metadata
pulumi config set aws:skipMetadataApiCheck false

# for New Relic
# https://www.pulumi.com/registry/packages/newrelic/installation-configuration/#configuring-credentials
pulumi env set $C pulumiConfig.newrelic:accountId 123ABC
pulumi env set $C pulumiConfig.newrelic:apiKey 123ABC --secret
pulumi env set $C pulumiConfig.newrelic:adminApiKey 123ABC --secret

# for Pinecone
# https://www.pulumi.com/registry/packages/pinecone/installation-configuration/#configuration
# re-use the same key defined in ${E} by importing it
pulumi env edit $C
# // to the very top of the Environment add the following:
# 
# imports:
#  - my-cool-chat-app-env
# 
# // save and exit the editor
pulumi env set $C pulumiConfig.pinecone:APIKey \${environmentVariables.PINECONE_API_KEY}

# preview infra, confirm "yes"
# pulumi config env add $C --stack dev --yes
# // example output
# KEY                       VALUE
# aws:profile               work
# aws:region                us-west-2
# newrelic:accountId        123ABC
# newrelic:adminApiKey      [secret]
# newrelic:apiKey           [secret]
# pinecone:APIKey           [secret]

# ENVIRONMENT VARIABLE   VALUE
# NEW_RELIC_LICENSE_KEY  [secret]
# OPENAI_API_KEY         [secret]
# PINECONE_API_KEY       [secret]

pulumi up --stack dev --yes

```

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
