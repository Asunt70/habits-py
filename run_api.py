import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graphs import year_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """returns a dict and pushs it to frontend"""
    data = year_data("2025")
    formatted_data = data.to_dict(orient="records")
    return formatted_data


if __name__ == "__main__":
    uvicorn.run("run_api:app", host="127.0.0.1", port=8000, reload=False)
