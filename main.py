import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import os
from enum import Enum


class ModelName(str, Enum):
    presidio = "presidio"


class AnonymizePayload(BaseModel):
    text: str
    model: str | None = ModelName.presidio


# load environment variables
port = os.environ["PORT"]

# initialize FastAPI
app = FastAPI(
    title="anonymize-app",
    description="Remove personally identifiable information from text. See [the project on GitHub](https://github.com/rodekruis/anonymization-app).",
    version="0.0.1",
    contact={
        "name": "NLRC 510",
        "url": "https://www.510.global/",
        "email": "support@510.global",
    },
    license_info={
        "name": "AGPL-3.0 license",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)

# Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


@app.get("/")
def index():
    return {"data": "Application ran successfully - FastAPI release v2.0"}


@app.post("/anonymize/")
async def anonymize_text(payload: AnonymizePayload):
    if payload.model == ModelName.presidio:
        analyzer_results = analyzer.analyze(
            text=payload.text,
            score_threshold=0.,
            language='en')
        anonymized_results = anonymizer.anonymize(
            text=payload.text,
            analyzer_results=analyzer_results
        )
        anonymized_text = anonymized_results.text
    else:
        raise HTTPException(status_code=404, detail=f"Model {payload.model} not found")

    return {"anonymized_text": anonymized_text}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.presidio:
        return {"model_name": model_name, "source": "https://microsoft.github.io/presidio/"}
    else:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)