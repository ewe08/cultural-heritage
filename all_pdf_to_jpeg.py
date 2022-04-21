from pdf2image import convert_from_path, convert_from_bytes
import requests
import sqlite3
import fitz
import pdfkit


conn = sqlite3.connect('db/Culture.db')
cursor = conn.cursor()
res = cursor.execute("SELECT id, photo FROM Products").fetchall()
for el in res:
    url = el[1]
    pdf = pdfkit.from_url(url)
    doc = fitz.open('out.pdf')
    page = doc.loadPage(0)  # number of page
    pix = page.get_pixmap()
    output = f"{el[0]}.jpeg"
    pix.save(output)


