import logging
import re
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from src.datastore.datastore import add_contact, contact_exists, get_paginated_contacts

router = APIRouter(
    prefix="/api",
    tags=["API"],
    responses={404: {"description": "Not found"}},
)


@router.get("/health")
def health():
    return "working"


class Contact(BaseModel):
    name: str
    email: str
    code: str
    number: str | int

    @field_validator("email")
    def validate_email(cls, value):
        pattern = r"^[a-zA-Z\d]([a-zA-Z\d\.\-_+%]*[a-zA-Z\d])?@[a-zA-Z\d]([a-zA-Z\d\-]*[a-zA-Z\d])?\.[a-zA-Z\d]{2,}$"
        if not bool(re.match(pattern, value)):
            raise ValueError("Email id is not in right format.")
        return value

    @field_validator("number")
    def validate_number(cls, value):
        if isinstance(value, int):
            value = str(value)
        pattern = r"^[\d]{10}$"
        if not bool(re.match(pattern, value)):
            raise ValueError("Phone number is not valid.")
        return value


@router.post("/contacts", response_model=Contact)
def add_contacts(request: Contact):
    try:
        contact_info = request.model_dump()
        if contact_exists(contact_info["number"]):
            logging.info(f"Contact '{contact_info['number']}' not added already exists")
            raise HTTPException(status_code=409, detail="Contact already exists")
        logging.info(f"Contact added: {contact_info}")
        add_contact(contact_info)
        return request
    except Exception as e:
        logging.error(f"Error in add contacts: \n\t{e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")


class GetContactResponse(BaseModel):
    contacts: list[Contact]
    page: int
    next: Optional[int]
    prev: Optional[int]
    limit: int
    total: int


@router.get("/contacts", response_model=GetContactResponse)
def get_contacts(page: int, limit: int):
    try:
        logging.info(f"Contact request with page: {page}, limit: {limit}.")
        res = get_paginated_contacts(page, limit)
        return GetContactResponse(
            contacts=[Contact(**contact) for contact in res["contacts"]],
            **{k: v for k, v in res.items() if k != "contacts"},
        )
    except Exception as e:
        logging.error(f"Error in get contacts: \n\t{e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@router.get("/search")
def search_contact():
    pass
