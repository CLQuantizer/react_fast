from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from .database import(
    add_journal,
    delete_journal,
    get_journal,
    get_journals,
    update_journal,
)

from .journal_schema import(
    ErrorResponseModel,
    ResponseModel,
    JournalSchema,
    UpdateJournalSchema,
)

router = APIRouter()

@router.post("/", response_description="Journal data added into the database")
async def add_journal_data(journal: JournalSchema = Body(...)):
    journal = jsonable_encoder(journal)
    new_journal = await add_journal(journal)
    return ResponseModel(new_journal, "Journal added successfully.")

@router.get("/", response_description="All journals data")
async def get_journals_data():
    journals = await get_journals()
    if journals:
        return ResponseModel(journals, "Journals retrieved successfully.")
    return ResponseModel(journals, 'Empty bro')

@router.get("/{id}", response_description="Single journal data retrieved")
async def get_journal_data(id):
    journal = await get_journal(id)
    if journal:
        return ResponseModel(journal, "Single journal data retrieved")
    return ErrorResponseModel("An error occurred", 404, "Student aint exist.")

@router.put("/{id}")
async def update_journal_data(id: str, req: UpdateJournalSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print('go stuck at the router')
    updated_journal = await update_journal(id, req)
    if updated_journal:
        return ResponseModel(
            "Journal with ID: {} name update is successful".format(id),
            "Journal name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Journal data.",
    )



