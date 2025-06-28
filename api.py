# api.py
import uvicorn
import webbrowser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global store for the data
shared_data = None


@app.get("/")
def root():
    """Return pushed data to frontend"""
    if shared_data is None:
        return JSONResponse(content={"error": "No data yet"}, status_code=404)
    return JSONResponse(content=shared_data)


def push_data(data):
    global shared_data
    shared_data = data.to_dict(orient="records")
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
