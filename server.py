from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="3GPP AI Agent API")

# -----------------------------
# Enable CORS (important for connectors)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load 3GPP Data
# -----------------------------
DATA = []

try:
    with open("3gpp_chunks.json", "r") as f:
        DATA = json.load(f)
except Exception as e:
    print(f"Error loading 3gpp_chunks.json: {e}")


# -----------------------------
# Request Model
# -----------------------------
class Query(BaseModel):
    query: str


# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "3GPP AI Agent API is running"}


# -----------------------------
# Main Search Endpoint
# -----------------------------
@app.post("/search_3gpp_spec")
def search_spec(data: Query):
    query = data.query.lower()
    results = []

    for item in DATA:
        text = item.get("text", "").lower()
        title = item.get("title", "").lower()
        clause = item.get("clause", "").lower()

        if query in text or query in title or query in clause:
            results.append(item)

    return {"results": results[:3]}


# -----------------------------
# Render-Compatible Startup
# -----------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
