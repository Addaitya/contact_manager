import csv
import os
import re
from itertools import islice

import pandas as pd

FILE_PATH = os.getenv("CONTACT_PATH", "src/datastore/contact.csv")


def get_paginated_contacts(page: int, limit: int) -> dict:
    """Returns pagenated record of contacts"""
    global FILE_PATH

    with open(FILE_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        start = page * limit
        end = start + limit

        contacts = [row for row, _ in zip(islice(reader, start, end), range(limit))]

        f.seek(0)
        reader = csv.DictReader(f)
        total = sum(1 for _ in reader)

        next_page = page + 1 if end < total else None
        prev_page = page - 1 if page > 0 else None

    return {
        "contacts": contacts,
        "page": page,
        "next": next_page,
        "prev": prev_page,
        "limit": limit,
        "total": total,
    }


def add_contact(contact: dict):
    """Add contact to csv file."""
    global FILE_PATH
    fieldnames = list(contact.keys())

    with open(FILE_PATH, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        file.seek(0, os.SEEK_END)  # move to last line

        # if file is empty add header line
        if file.tell() == 0:

            writer.writeheader()

        writer.writerow(contact)


def contact_exists(number: str):
    global FILE_PATH
    with open(FILE_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["number"] == number:
                return True

    return False


def delete_contact(number: str):
    global FILE_PATH
    temp_file = FILE_PATH + ".tmp"

    with open(FILE_PATH, "r") as inp, open(temp_file, "w") as out:
        reader = csv.DictReader(inp)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row["number"] != number:
                writer.writerow(row)

    os.replace(temp_file, FILE_PATH)


def search_contact(query: str):
    global FILE_PATH
    df = pd.read_csv(FILE_PATH)

    query = query.strip()
    # search email field
    if bool(re.match(r"^[\s]*@[\s*]$", query)):
        result = df[df["email"].str.contains(query, case=False, na=False)].to_dict(
            "records"
        )
    # search in number field
    elif bool(re.match(r"^[\d]+$", query)):
        result = df[
            df["number"].astype(str).str.contains(str(query), case=False, na=False)
        ].to_dict("records")
    # search in name field
    else:
        result = df[df["name"].str.contains(query, case=False, na=False)].to_dict(
            "records"
        )

    return result
