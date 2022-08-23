# anonymization-app
Remove personally identifiable information from text, at scale, using AI.

See it action and test it yourself on [the demo version](https://rodekruis-anonymization-app-demo-b7gim4.streamlitapp.com/).

The API is publicly accessible at [https://anonymization-app.azurewebsites.net/](https://anonymization-app.azurewebsites.net/).

## Description

Synopsis: a [dockerized](https://www.docker.com/) [python](https://www.python.org/) API that removes personally identifiable information (PII) from text.

Worflow: POST some text and receive it back without PII.

## API Usage

See [the documentation](https://anonymization-app.azurewebsites.net/docs).

## Models

All models are basically neural networks trained to perform [Named Entity Recognition (NER)](https://en.wikipedia.org/wiki/Named-entity_recognition). Specifically, they look for person names in text. The following models are currently supported:
- **ensemble** (default and recommended): use all available models
- **[presidio](https://microsoft.github.io/presidio/)**: fancy regex + [spaCy](https://spacy.io/) models for NER. Built and maintained by Microsoft.
- **[BERT](https://huggingface.co/dslim/bert-base-NER)**: BERT model, fine-tuned for NER. Open-source, hosted by HuggingFace.

## Setup

From project root, run locally with `pipenv run python main.py`.

Deploy with [Azure Web Apps](https://azure.microsoft.com/en-us/services/app-service/web/) to serve publicly, for example as explained [here](https://medium.com/nerd-for-tech/deploying-a-simple-fastapi-in-azure-79c59c430064).

