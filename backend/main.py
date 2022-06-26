import gensim.downloader
import pickle
import secrets
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi import Depends,Request, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from users.router import userRouter

app = FastAPI()
app.include_router(userRouter, tags=["User"], prefix="/users")


origins = [
    "http://139.162.225.136",
    "http://langedev.net",
    "http://langedev.net:3000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

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

@app.get("/related/")
async def related():
    words = ['Sorry 🥵', 'Please input']
    probs = ['','something']
    return {'words':words, 'probs':probs}
