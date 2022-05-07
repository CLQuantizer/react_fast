import pandas as pd
import gensim.downloader
import pickle
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List
from fastapi import Depends,Request, FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://langedev.net",
    "http://langedev.net:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

glove_vectors = gensim.downloader.load('glove-wiki-gigaword-50')

with open('glove50','wb') as f:
    pickle.dump(glove_vectors,f)
with open('glove50','rb') as f:
    glove_vectors = pickle.load(f)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

@app.post("/related/{word}")
async def related(word):
	word = word.lower()
	df = pd.DataFrame(glove_vectors.most_similar(word,topn=15),columns = ['words','sim'])
	words = list(df['words'])
	probs = [round(x,2) for x in list(df['sim'])]
	return {'words':words, 'probs':probs}