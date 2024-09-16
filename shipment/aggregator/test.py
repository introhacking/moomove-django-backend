

from docx import Document
import json

def extract_table_data(doc_path):
    doc = Document(doc_path)
    tables = doc.tables

    # Assuming the table you want is the first table in the document
    table = tables[0]

    data = []
    keys = None

    for i, row in enumerate(table.rows):
        text = [cell.text.strip() for cell in row.cells]
        if i == 0:
            keys = text  # assuming first row as header
        else:
            data.append(dict(zip(keys, text)))

    return data

