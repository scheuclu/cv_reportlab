from reportlab.pdfgen import canvas
import yaml

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter

FONTSIZE_SECTION=12
FONTGAP_SECTION=1.2

FONTSIZE_BODY=10
FONTGAP_BODY=1.2

MARGIN_LEFT=20
MARGIN_RIGHT=20
MARGIN_TOP=40

# Define a style for the bulleted list
styles = getSampleStyleSheet()
bullet_style = ParagraphStyle(
    "BulletStyle",
    parent=styles["BodyText"],
    spaceBefore=6,
    bulletIndent=20,
    leftIndent=10,
    bulletFontName="Helvetica",
    bulletFontSize=10,
)


def print_points(pdf, points,  xmin, ystart, font="Helvetica", font_size=10):
    pdf.setFont(font, font_size)
    y=ystart
    for item in points:
        paragraph = Paragraph(f"• {item}", bullet_style)
        paragraph.wrapOn(pdf, width - MARGIN_RIGHT, xmin)
        print(paragraph.blPara.lines)
        try:
            for x, text in paragraph.blPara.lines:
                pdf.drawString(xmin, y, ' '.join(text))
                y -= font_size
        except:
            pass
    return y



if __name__ == "__main__":
    # Specify the file path for the PDF
    pdf_file = "example.pdf"



    infile='cv.yaml'
    with open(infile, "r") as f:
        t=f.read()
        #t=markdown_links(t)
        try:
            cv = yaml.safe_load(t)
            ###print(result)
        except yaml.YAMLError as exc:
            print(exc)


    pdf = canvas.Canvas(pdf_file, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    # Set the starting point for writing


    width, height = letter
    center_x = width / 2
    y = height-MARGIN_TOP

    pdf.setFont("Helvetica-Bold", 32)
    headline_text="Lukas <b>bold</b> Scheucher"
    x_coordinate = (width - pdf.stringWidth(headline_text, "Helvetica-Bold", 16)) / 2
    pdf.drawCentredString(x_coordinate, y, headline_text)
    y-=32
    pdf.setFont("Helvetica", 12)
    pdf.drawString(MARGIN_LEFT, y, "lukas@scheuclu.com | (+43)-677-6100-3595 | scheuclu | scheuclu")
    y -= 28

    pdf.setFont("Helvetica", 12)

    for section in cv['sections']:
        heading=section['heading']
        print(heading)
        subsections=section['subsections'] if 'subsections' in section else []
        points=section['points'] if 'points' in section else []
        print(points)


        text_width = pdf.stringWidth(heading, "Helvetica", 12)
        x = center_x - (text_width / 2)
        pdf.line(MARGIN_LEFT, y+6, x-FONTSIZE_SECTION, y+6)
        pdf.drawString(x, y, heading)
        pdf.line(x+text_width+FONTSIZE_SECTION, y + 6, width-MARGIN_RIGHT, y + 6)
        y -= int(FONTSIZE_SECTION*FONTGAP_SECTION*2)
        y = print_points(pdf, points, MARGIN_LEFT, ystart=y, font="Helvetica", font_size=10)

        for subsection in subsections:
            subsection_heading=subsection['heading']['label']
            subsection_points = subsection['points'] if 'points' in subsection else []
            print(subsection.keys())
            pdf.drawString(MARGIN_LEFT, y, subsection_heading)
            y -= FONTSIZE_SECTION * FONTGAP_SECTION

            # pdf.setFont("Helvetica", 10)
            # for item in subsection_points:
            #     paragraph = Paragraph(f"• {item}", bullet_style)
            #     paragraph.wrapOn(pdf, width-MARGIN_RIGHT, MARGIN_LEFT)
            #     print(paragraph.blPara.lines)
            #     for x, text in paragraph.blPara.lines:
            #         pdf.drawString(MARGIN_LEFT, y, ' '.join(text))
            #         y -= 10
            y=print_points(pdf, subsection_points, xmin=MARGIN_LEFT, ystart=y, font="Helvetica", font_size=10)
            pdf.setFont("Helvetica", 12)
                # y -= max(paragraph.height*(len(paragraph.blPara.lines)-1),0)# Adjust width as needed
                # paragraph.drawOn(pdf, MARGIN_LEFT, y)
                # y -= paragraph.height*len(paragraph.blPara.lines)
                #y -= FONTSIZE_SECTION * FONTGAP_SECTION
                #break

        #break

    pdf.save()

    print(f"PDF created successfully: {pdf_file}")