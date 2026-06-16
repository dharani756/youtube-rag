from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
from urllib.parse import urlparse, parse_qs
from google import genai
from dotenv import load_dotenv
import numpy as np
import faiss
import os

# Load .env
load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Embedding Model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chunks_store = []
faiss_index = None


# Request Models
class VideoRequest(BaseModel):
    youtube_url: str


class QuestionRequest(BaseModel):
    question: str


# Extract Video ID
def extract_video_id(url):

    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]

    if "youtube.com" in url:
        parsed_url = urlparse(url)
        return parse_qs(
            parsed_url.query
        )["v"][0]

    return url


# Split Transcript
def split_text(text, chunk_size=500):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):
        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


# Home
@app.get("/")
def home():

    return {
        "message": "YouTube RAG Running"
    }


# Process Video
@app.post("/process-video")
def process_video(
    data: VideoRequest
):

    global chunks_store
    global faiss_index

    video_id = extract_video_id(
        data.youtube_url
    )

    print(
        "VIDEO ID =",
        video_id
    )

    api = YouTubeTranscriptApi()

    try:

        transcript = api.fetch(
            video_id,
            languages=["en"]
        )

    except:

        try:

            transcript = api.fetch(
                video_id,
                languages=["te"]
            )

        except Exception as e:

            return {
                "error": str(e)
            }

    text = " ".join(
        [
            snippet.text
            for snippet in transcript
        ]
    )

    chunks_store = split_text(
        text
    )

    embeddings = embedding_model.encode(
        chunks_store
    )

    dimension = embeddings.shape[1]

    faiss_index = faiss.IndexFlatL2(
        dimension
    )

    faiss_index.add(
        np.array(
            embeddings,
            dtype=np.float32
        )
    )

    return {
        "message":
        "Video Processed Successfully",
        "chunks":
        len(chunks_store)
    }


# Ask Question
@app.post("/ask")
def ask_question(data: QuestionRequest):

    global faiss_index

    if faiss_index is None:
        return {
            "error": "Please process a video first"
        }

    query_embedding = embedding_model.encode(
        [data.question]
    )

    D, I = faiss_index.search(
        np.array(
            query_embedding,
            dtype=np.float32
        ),
        k=min(3, len(chunks_store))
    )

    results = []

    for idx in I[0]:
        results.append(
            chunks_store[idx]
        )

    context = "\n".join(results)

    prompt = f"""

Context:
{context}

Question:
{data.question}

Answer in the language requested by the user.
Translate if necessary.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "answer": response.text
        }

    except Exception as e:

        

            return {
        "answer": context,
        "gemini_error": str(e)
    }