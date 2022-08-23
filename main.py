import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re
import os
from enum import Enum


class ModelName(str, Enum):
    ensemble = "ensemble"
    presidio = "presidio"
    BERT = "BERT"

    @classmethod
    def exists(cls, key):
        return key in cls.__members__


class AnonymizePayload(BaseModel):
    text: str
    model: str = ModelName.ensemble


# load environment variables
port = os.environ["PORT"]

# initialize FastAPI
app = FastAPI(
    title="anonymize-app",
    description="Remove personally identifiable information from text. \n"
                "Built with love by [NLRC 510](https://www.510.global/). See [the project on GitHub](https://github.com/rodekruis/anonymization-app) or [contact us](mailto:support@510.global).",
    version="0.0.1",
    license_info={
        "name": "AGPL-3.0 license",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)

# Initialize presidio
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Initialize BERT
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER-uncased")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER-uncased")
pipe = pipeline(model=model, tokenizer=tokenizer, task='ner')


@app.get("/")
def index():
    return {"data": "Welcome to anonymize-app!"}


@app.post("/anonymize/")
async def anonymize_text(payload: AnonymizePayload):
    text = payload.text

    if payload.model == ModelName.ensemble or payload.model == ModelName.presidio:
        analyzer_results = analyzer.analyze(
            text=text,
            score_threshold=0.,
            language='en'
        )
        anonymized_results = anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results
        )
        text = anonymized_results.text

    if payload.model == ModelName.ensemble or payload.model == ModelName.BERT:
        entities = pipe(text)
        # replace detected names (entity: person) with ~~~~
        for entity in entities:
            if entity['entity'] in ['B-PER', 'I-PER']:
                text = text[:entity['start']] + '~' * (entity['end'] - entity['start']) + text[entity['end']:]
        # replace ~~~~ with <PERSON>
        names_masks = []
        for match in re.finditer(r"(~)+", text):
            names_masks.append(match.group())
        names_masks.sort(key=lambda s: len(s), reverse=True)
        for name_mask in names_masks:
            text = text.replace(name_mask, "<PERSON>")

    if not ModelName.exists(payload.model):
        raise HTTPException(status_code=404, detail=f"Model {payload.model} not found")

    # merge multiple names into one
    for pattern in ["<PERSON><PERSON>", "<PERSON> <PERSON>"]:
        while pattern in text:
            text = text.replace(pattern, '<PERSON>')

    return {"anonymized_text": text}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.ensemble:
        return {"model_name": model_name, "source": "combination of all other models"}
    elif model_name == ModelName.presidio:
        return {"model_name": model_name, "source": "https://microsoft.github.io/presidio/"}
    elif model_name == ModelName.BERT:
        return {"model_name": model_name, "source": "https://huggingface.co/dslim/bert-base-NER"}
    else:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)