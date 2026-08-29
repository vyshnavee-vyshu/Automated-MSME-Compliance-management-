from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gst_scraper import scrape_gst_updates


app = FastAPI(
    title="MSME GST Compliance API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "MSME GST Compliance API is running"
    }


@app.get("/api/gst/updates")
def get_gst_updates():
    return scrape_gst_updates()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )