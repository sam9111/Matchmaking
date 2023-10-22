
import uvicorn

from fastapi import Body, FastAPI
import json
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def create_vector(sample):

    with open('card_data.json') as json_file:

        card_data = json.load(json_file)

    everything = []

    for category in card_data.keys():
        everything.append(category)
        everything += card_data[category]["skills"]
        everything += card_data[category]["interests"]

    indices = []

    for element in sample:

        indices.append(everything.index(element))

    vector = [0] * len(everything)

    for index in indices:

        vector[index] = 1

    return vector


@app.post("/matches")
def generate_matches(mentee: list = Body(...)):

    if len(mentee) == 0:
        return {"matches": []}

    with open('random_mentors.json') as json_file:

        random_mentors = json.load(json_file)

    scores = []

    for mentor in random_mentors:

        vector = create_vector(random_mentors[mentor]["categories"] +
                               random_mentors[mentor]["skills"] + random_mentors[mentor]["interests"])

        score = cosine_similarity([create_vector(mentee)], [
            vector])[0][0]

        scores.append({"mentor": mentor, "score": score})

    top5 = sorted(scores, key=lambda x: x["score"], reverse=True)[:3]

    return {"matches": top5}
