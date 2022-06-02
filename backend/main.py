import gensim.downloader
import pickle
import secrets
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi import Depends,Request, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from journal.journal_router import router as JournalRouter

app = FastAPI()
app.include_router(JournalRouter, tags=["Journal"], prefix="/journal")

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



app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# glove_vectors = gensim.downloader.load('glove-wiki-gigaword-50')

# with open('glove50','wb') as f:
#     pickle.dump(glove_vectors,f)
with open('glove50','rb') as f:
    glove_vectors = pickle.load(f)

@app.get("/")
async def read_main(token: str = Depends(oauth2_scheme)):
    return {"msg": "Hello World", "token":token}

@app.get("/related/{Word}")
async def related(Word):
    word = Word.lower().strip()
    if word in glove_vectors.key_to_index:
        wordsnprobs= glove_vectors.most_similar(word,topn=15)
        words = [pair[0] for pair in wordsnprobs]
        probs = [round(pair[1],2) for pair in wordsnprobs]

    else:
        words = ['Sorry 🥵', 'This input', 'is not a word']
        probs = ['','\''+Word+'\'', 'or is too rare for this little app']
    return {'words':words, 'probs':probs}

@app.post("/related/")
async def related():
    words = ['Sorry 🥵', 'Please input']
    probs = ['','something']
    return {'words':words, 'probs':probs}
