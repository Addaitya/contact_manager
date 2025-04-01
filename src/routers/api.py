from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["API"],
    responses={404: {"description": "Not found"}},
)


@router.get("/health")
def health():
    return "working"

@router.post("/contacts")
def add_contact():
    pass

@router.get('/contacts')
def get_contacts():
    pass

@router.get('/search')
def search_contact():
    pass