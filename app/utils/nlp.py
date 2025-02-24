from pydantic import BaseModel
from gliner import GLiNER

gliner_model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1", max_length=768)


class NER_Entity(BaseModel):
    start: int
    end: int
    text: str
    label: str
    score: float


def nlp_tokens(text):
    token_generator = gliner_model.data_processor.words_splitter(text)
    tokens = [t for t in token_generator]
    return len(tokens)
