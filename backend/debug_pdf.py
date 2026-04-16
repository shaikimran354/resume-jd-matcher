import pdfplumber
import io

with open('C:\\Users\\Praveen Dangi\\Downloads\\PraveenDangi.pdf', 'rb') as f:
    data = f.read()

with pdfplumber.open(io.BytesIO(data)) as pdf:
    text = ''
    for page in pdf.pages:
        t = page.extract_text()
        if t:
            text += t

print(repr(text[:1000]))