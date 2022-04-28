# Simple Wordle - Backend

Backend API application for my Simple Wordle application.

Built using [FastAPI](https://fastapi.tiangolo.com/)

## Demo application

A demo is accessible at [https://bagaze-wordle-backend.herokuapp.com/docs](https://bagaze-wordle-backend.herokuapp.com/docs)

## Build and run

### To run locally:

Clone the repository and perform the following commands:

```
cp env-sample ./.env
poetry install
poetry run start
```

App is accessible at: [http://localhost:8080](http://localhost:8080)
Doc is accessible at: [http://localhost:8080/docs](http://localhost:8080/docs)

### Through Docker

#### Development

```
cp env-sample ./local-env
docker-compose build
docker-compose up
```

App is accessible at: [http://localhost:9090](http://localhost:9090)
Doc is accessible at: [http://localhost:9090/docs](http://localhost:9090/docs)
