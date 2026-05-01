from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest,query,chat,research


app = FastAPI(title= "AKS API",
              description="AI knowledge System backend",
              version="0.1.0")

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:3000"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])




app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(chat.router)
app.include_router(research.router)





@app.get("/")
async def root():
    return {"message": "Welcome to PAKS — Personal AI Knowledge System"}


@app.get("/health")
async def health_check():
    return {
  "status": "ok",
  "service": "AKS API",
  "version": "0.1.0"
}
