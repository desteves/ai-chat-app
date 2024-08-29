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
pulumi login
pulumi up
```

## Run Locally

Additional requirements:

- Docker
- A Pinecone index named `games` in the `default` namespace that needs to use the `text-embedding-ada-002` model
- Update the `dashboard.json` accountIds array to include YOUR New Relic account id
- Import the `dashboard.json` to your New Relic account
- Create .env files as shown in the [docker-compose.yml](./app/docker-compose.yml) comments

```bash
cd app
docker compose up --build
```

## Acknowledgements

This repo stems from existing work by @harrykimpel

- [Node Chat Service](https://github.com/harrykimpel/node-chat-service)
- [Chat Front-End](https://github.com/harrykimpel/python-flask-openai/tree/main/chat-frontend)
