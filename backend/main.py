import pandas as pd
import gensim.downloader
import pickle
from typing import List
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends,Request, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://langedev.net",
    "http://langedev.net:3000",
    "http://langedev.net:80",
    "localhost:3000",
    "localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# glove_vectors = gensim.downloader.load('glove-wiki-gigaword-50')

# with open('glove50','wb') as f:
#     pickle.dump(glove_vectors,f)
with open('glove50','rb') as f:
    glove_vectors = pickle.load(f)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

@app.post("/related/{Word}")
async def related(Word):
    word = Word.lower().strip()
    if word in glove_vectors.key_to_index:
        df = pd.DataFrame(glove_vectors.most_similar(word,topn=15),columns = ['words','prob'])
        words = list(df['words'])
        probs = [round(x,2) for x in list(df['prob'])]
    else:
        words = ['Sorry 🥵', 'This input', 'is not a word']
        probs = ['','\''+Word+'\'', 'or is too rare for this little app']
    return {'words':words, 'probs':probs}

@app.post("/related/")
async def related():
    words = ['Sorry 🥵', 'Please input']
    probs = ['','something']
    return {'words':words, 'probs':probs}
