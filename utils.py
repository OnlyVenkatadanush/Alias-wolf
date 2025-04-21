# utils.py

import pandas as pd
from datetime import datetime
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_results(df, filetype="csv"):
    buffer = BytesIO()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if filetype == "csv":
        df.to_csv(buffer, index=False)
    elif filetype == "excel":
        df.to_excel(buffer, index=False)
    
    buffer.seek(0)
    return buffer

def export_to_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    textobject = c.beginText(40, height - 50)
    textobject.setFont("Helvetica", 12)

    for index, row in df.iterrows():
        line = f"{row['site']} - {row['status']} - {row['url']}"
        textobject.textLine(line)
    
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
