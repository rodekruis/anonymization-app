# anonymization-app
Remove personally identifiable information from text.

API is publicly accessible at [https://anonymization-app.azurewebsites.net/](https://anonymization-app.azurewebsites.net/).

## Description

Synopsis: a [dockerized](https://www.docker.com/) [python](https://www.python.org/) API that removes personally identifiable information (PII) from text.

Worflow: send text and receive text without PII.

## Usage

See it in action here (TBI).

Use it via API as per [documentation](https://anonymization-app.azurewebsites.net/docs).

## Setup

From project root, run locally with `pipenv run python main.py`.

Deploy with [Azure Web Apps](https://azure.microsoft.com/en-us/services/app-service/web/) to serve publicly, for example as explained [here](https://medium.com/nerd-for-tech/deploying-a-simple-fastapi-in-azure-79c59c430064).

