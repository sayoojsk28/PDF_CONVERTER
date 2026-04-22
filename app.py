import streamlit as st
from docx import Document
from reportlab.pdfgen import canvas
from io import BytesIO

st.title("TXT / DOCX to PDF Converter")

uploaded_file = st.file_uploader(
    "Upload TXT or DOCX",
    type=["txt", "docx"]
)

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

def create_pdf(text):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50

    usable_width = width - left_margin - right_margin

    y = height - top_margin
    font_name = "Helvetica"
    font_size = 12

    pdf.setFont(font_name, font_size)

    for paragraph in text.split("\n"):

        words = paragraph.split(" ")
        line = ""

        for word in words:
            test_line = line + word + " "

            if stringWidth(test_line, font_name, font_size) <= usable_width:
                line = test_line
            else:
                pdf.drawString(left_margin, y, line)
                y -= 20
                line = word + " "

                if y < bottom_margin:
                    pdf.showPage()
                    pdf.setFont(font_name, font_size)
                    y = height - top_margin

        if line:
            pdf.drawString(left_margin, y, line)
            y -= 20

        if y < bottom_margin:
            pdf.showPage()
            pdf.setFont(font_name, font_size)
            y = height - top_margin

    pdf.save()
    buffer.seek(0)
    return buffer

if uploaded_file is not None:

    file_text = ""

    # Read TXT
    if uploaded_file.name.endswith(".txt"):
        file_text = uploaded_file.read().decode("utf-8")

    # Read DOCX
    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            file_text += para.text + "\n"

    # Original file button
    if st.button("Use Uploaded File"):
        pdf_file = create_pdf(file_text)

        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="converted.pdf",
            mime="application/pdf"
        )

    st.subheader("Edit Content If Needed")

    edited_text = st.text_area(
        "Modify below text",
        value=file_text,
        height=300
    )

    # Show only after edit
    if edited_text != file_text:

        if st.button("Use Edited Content"):
            pdf_file = create_pdf(edited_text)

            st.download_button(
                label="Download Edited PDF",
                data=pdf_file,
                file_name="edited_converted.pdf",
                mime="application/pdf"
            )