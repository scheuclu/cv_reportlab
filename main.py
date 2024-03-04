from reportlab.pdfgen import canvas
import yaml
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus.flowables import HRFlowable, KeepTogether
import os

from utils import bullet_points


import re

FONTSIZE_SECTION = 12
FONTGAP_SECTION = 1.2

FONTSIZE_BODY = 10
FONTGAP_BODY = 1.2

MARGIN_LEFT = 20
MARGIN_RIGHT = 20
MARGIN_TOP = 40


styles = getSampleStyleSheet()
style_section = styles["Heading3"].clone("section")
style_section.fontName = "Helvetica-Bold"
style_section.fontSize = 14
style_section.spaceBefore = 16


style_subsection = styles["Heading4"].clone("section")
style_subsection.leading = 0
style_subsection.spaceAfter = 0
style_subsection.spaceBefore = 12
style_subsection.fontName = "Helvetica-bold"


style_date = styles["BodyText"].clone("date")
style_date.alignment = 2  # 0=left, 1=center, 2=right
style_date.spaceBefore = 0
style_date.spaceAfter = 4


style_section_points = styles["Normal"].clone("style_section_points")
style_subsection_points = styles["Normal"].clone("style_section_points")

style_cv_title = styles["Heading1"].clone("style_cv_title")
style_cv_title.fontSize = 28
style_cv_title.spaceAfter = 14
# style_cv_title.textColor='#092f61'


style_socials = styles["Normal"].clone("style_socials")
# style_socials.textColor='#092f61'


def header(name, mail=None, phone=None, github=None, linkedin=None):
    lines = []
    title = Paragraph(name, style_cv_title)
    lines.append(title)
    symbols = []
    if mail:
        symbols.append(
            f'<a href="mailto:{mail}"><img src="resources/mail-icon.png" height="4mm" width="4mm"/>   <b>{mail}</b></a>'
        )
    if phone:
        symbols.append(
            f'<a href="tel: {phone}"><img src="resources/phone-icon.png" height="4mm" width="4mm"/>   <b>{phone}</b></a>'
        )
    if github:
        symbols.append(
            f'<a href="https://www.github.com/{github}"><img src="resources/github-icon.png" height="4mm" width="4mm"/>   <b>{github}</b></a>'
        )
    if linkedin:
        symbols.append(
            f'<a href="https://www.linkedin.com/in/{linkedin}"><img src="resources/linkedin-icon.png" height="4mm" width="4mm"/>   <b>{linkedin}</b></a>'
        )

    lines.append(Paragraph("&nbsp;&nbsp;|&nbsp;&nbsp;".join(symbols), style_socials))
    lines.append(
        HRFlowable(
            width="100%",
            thickness=2,
            lineCap="round",
            color="black",
            spaceBefore=12,
            spaceAfter=1,
        )
    )
    return lines


def process_file(yaml_path, pdf_path):
    # Specify the file path for the PDF
    # pdf_file = "example.pdf"

    document = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=30,
        bottomMargin=50,
    )

    # infile = "cv.yaml"
    with open(yaml_path, "r") as f:
        t = f.read()
        # t=markdown_links(t)
        try:
            cv = yaml.safe_load(t)
            ###print(result)
        except yaml.YAMLError as exc:
            print(exc)

    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    pdf.setFont("Courier-Oblique", 12)
    # Set the starting point for writing

    width, height = letter
    center_x = width / 2
    y = height - MARGIN_TOP

    doc = []
    title = Paragraph("Lukas Scheucher", style_cv_title)

    doc += header(
        name="Lukas Scheucher",
        mail="lukas@scheuclu.com",
        phone="0043-677-6100-3595",
        github="scheuclu",
        linkedin="scheuclu",
    )

    for section in cv["sections"]:
        heading = section["heading"]
        doc.append(Paragraph(f"<u>{heading}</u>", style_section))
        subsections = section["subsections"] if "subsections" in section else []
        section_points = section["points"] if "points" in section else []

        for subsection in subsections:
            subsection_heading = subsection["heading"]["label"]
            startdate = (
                subsection["heading"]["startdate"]
                if "startdate" in subsection["heading"]
                else None
            )
            enddate = (
                subsection["heading"]["enddate"]
                if "enddate" in subsection["heading"]
                else None
            )
            subsection_points = subsection["points"] if "points" in subsection else []
            subsection_degrees = (
                subsection["degrees"] if "degrees" in subsection else []
            )
            doc.append(Paragraph(subsection_heading, style_subsection))
            if startdate and enddate:
                doc.append(Paragraph(f"{startdate} - {enddate}", style_date))
            else:
                doc.append(Spacer(1, 12))
            doc += bullet_points(subsection_points, style=style_subsection_points)
            doc += bullet_points(subsection_degrees, style=style_subsection_points)
        doc += bullet_points(section_points, style=style_section_points)
        doc.append(
            HRFlowable(
                width="100%",
                thickness=1,
                lineCap="round",
                color="#bbbbbb",
                spaceBefore=12,
                spaceAfter=0,
            )
        )

    document.build(doc)
    print(f"PDF created successfully: {pdf_path}")


if __name__ == "__main__":
    for f in os.listdir("inputs"):
        if not f.endswith(".yaml"):
            continue
        yaml_path = f"inputs/{f}"
        pdf_path = f"outputs/{f.replace('.yaml','.pdf')}"
        process_file(yaml_path, pdf_path)
