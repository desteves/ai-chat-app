#docker run --rm -p 6379:6379 -d redis

node --no-lazy -r ts-node/register -r newrelic --preserve-symlinks ./src/index.ts