from fastapi import APIRouter
from models.schemas import IngestRequest,IngestResponse

router = APIRouter(prefix="/api/ingest",tags=["Ingestion"])

@router.post("/",response_model=IngestResponse,summary="ingesting a Doc")
async def ingest_document(request: IngestRequest):
    return IngestResponse( id="doc_001",
        filename=request.filename,
        status="success",
        chunks_created=5)

@router.get("/documents",summary="get teh Doc")
async def doc_return():
    return [
        {"id": "doc_001", "filename": "research.pdf"},
        {"id": "doc_002", "filename": "notes.md"}
    ]
