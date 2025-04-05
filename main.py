import os

import yaml
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus.flowables import HRFlowable
from reportlab.platypus import Image  # Import Image

from utils import bullet_points, simple_text

# Register a custom TrueType font
pdfmetrics.registerFont(TTFont("Calibri", "./calibri-regular.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-Bold", "./calibri-bold.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-Italic", "./calibri-italic.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-BoldItalic", "./calibri-bold-italic.ttf"))
# pdfmetrics.registerFontFamily(family="Calibri", normal=)

# Register the font family
pdfmetrics.registerFontFamily(
    "Calibri",
    normal="Calibri",
    bold="Calibri-Bold",
    italic="Calibri-Italic",
    boldItalic="Calibri-BoldItalic"
)


FONTSIZE_SECTION = 12
FONTGAP_SECTION = 1.2

FONTSIZE_BODY = 10
FONTGAP_BODY = 1.2

MARGIN_LEFT = 10
MARGIN_RIGHT = 10
MARGIN_TOP = 40


# def get_style(
#         font:str,
#         size:int,
#         spaceBefore:int,
#         color: str = '#000000'
# )


styles = getSampleStyleSheet()
style_section = styles["Heading3"].clone("section")
style_section.fontName = "Calibri-Bold"
style_section.fontSize = 14
style_section.spaceBefore = 16
style_section.textColor = "#303030"
style_section.underline = True  # Ensure links are underlined
# ---


style_subsection = styles["Heading4"].clone("section")
style_subsection.leading = 0
style_subsection.spaceAfter = 0
style_subsection.spaceBefore = 12
style_subsection.fontName = "Calibri-Bold"
style_subsection.underline = True  # Ensure links are underlined
# ---


style_date = styles["BodyText"].clone("date")
style_date.alignment = 2  # 0=left, 1=center, 2=right
style_date.spaceBefore = 0
style_date.spaceAfter = 4  # After founder in residence
# ---


style_section_points = styles["Normal"].clone("style_section_points")
style_section_points.fontName = "Calibri"
# ---

style_prompt = styles["Normal"].clone("style_prompt")
style_prompt.fontName = "Calibri"
style_prompt.fontSize = 1
style_prompt.textColor = "#ffffff"
# ---


style_subsection_points = styles["Normal"].clone("style_section_points")
style_subsection_points.fontName = "Calibri"
# ---

style_cv_title = styles["Heading1"].clone("style_cv_title")
style_cv_title.fontSize = 28
style_cv_title.spaceAfter = 14
style_cv_title.fontName = "Calibri"
# ---


style_socials = styles["Normal"].clone("style_socials")
# ---


def header(name, mail=None, phone=None, github=None, linkedin=None):
    lines = []
    title = Paragraph(name, style_cv_title)
    lines.append(title)
    symbols = []
    if mail:
        symbols.append(
            f'<a href="mailto:{mail}">\
                <img src="resources/email.png" height="4mm" width="4mm"/>   <b>{mail}</b></a>'
        )
    if phone:
        symbols.append(
            f'<a href="tel: {phone}">\
                <img src="resources/telephone.png" height="4mm" width="4mm"/>   <b>{phone}</b></a>'
        )
    if github:
        symbols.append(
            f'<a href="https://www.github.com/{github}">\
            <img src="resources/github.png" height="4mm" width="4mm"/>   <b>{github}</b></a>'
        )
    if linkedin:
        symbols.append(
            f'<a href="https://www.linkedin.com/in/{linkedin}">\
                <img src="resources/linkedin.png" height="4mm" width="4mm"/>   <b>{linkedin}</b></a>'
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
        leftMargin=20,
        rightMargin=20,
        topMargin=30,
        bottomMargin=50,
    )

    # infile = "cv.yaml"
    with open(yaml_path, "r") as f:
        t = f.read()
        # t=markdown_links(t)
        try:
            cv = yaml.safe_load(t)
        except yaml.YAMLError as exc:
            print(exc)

    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    # pdf.setFont("ZapfDingbats", 24)

    doc = []

    doc += header(
        name="Lukas Scheucher",
        mail="scheuclu@gmail.com",
        # phone="0043-677-6100-3595",
        github="scheuclu",
        linkedin="scheuclu",
    )

    for section in cv["sections"]:
        heading = section["heading"]


        heading_line = f"<u>{heading}</u>"
        # if 'logos' in section:
        #     for logo in section['logos']:
        #         heading_line+=f"<img src='{logo}' height='4mm' width='4mm' valign='middle'/> "
        doc.append(Paragraph(heading_line, style_section))

        subsections = section["subsections"] if "subsections" in section else []
        section_points = section["points"] if "points" in section else []
        section_text = section["text"] if "text" in section else []

        if 'bullets' in section:
            print(section['bullets'])
            assert 1==2

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

            subsetion_text = subsection["text"] if "text" in subsection else []

            if 'bullets' in subsection:
                print(subsection['bullets'])
                assert 1 == 2
            subsection_bullets=subsection["bullets"] if 'bullets' in subsection else []

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
            doc += simple_text(subsetion_text, style=style_subsection_points) #TODO
        doc += bullet_points(section_points, style=style_section_points)
        doc += simple_text(section_text, style=style_section_points)
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

    # img = Image('./logos/google.png', width=20, height=20)  # Adjust width and height as needed
    # # doc.append(img)
    # doc.append(Paragraph([heading_line, img], style_section))


    if 'prompt' in cv:
        print(cv['prompt'])
        for sentence in cv['prompt']:
            doc += simple_text(sentence, style=style_prompt)




    document.build(doc)
    print(f"PDF created successfully: {pdf_path}")


if __name__ == "__main__":
    for f in os.listdir("inputs"):
        if not f.endswith(".yaml"):
            continue
        yaml_path = f"inputs/{f}"
        pdf_path = f"outputs/{f.replace('.yaml','.pdf')}"
        process_file(yaml_path, pdf_path)
    from reportlab.pdfbase import pdfmetrics

    # Get a list of all registered fonts
    available_fonts = pdfmetrics.getRegisteredFontNames()

    # Print each font
    print("Available Fonts in ReportLab:")
    for font in available_fonts:
        print(font)


# test=['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__',
#       '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
#       '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
#       '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__',
#       '__subclasshook__', '__weakref__', '_setKwds', 'alignment', 'allowOrphans', 'allowWidows',
#       'backColor', 'borderColor', 'borderPadding', 'borderRadius', 'borderWidth', 'bulletAnchor'
#       'bulletFontName', 'bulletFontSize', 'bulletIndent', 'clone', 'defaults', 'embeddedHyphenation',
#       'endDots', 'firstLineIndent', 'fontName', 'fontSize', 'hyphenationLang', 'justifyBreaks',
#       'justifyLastLine', 'leading', 'leftIndent', 'linkUnderline', 'listAttrs', 'name', 'parent',
#       'refresh', 'rightIndent', 'spaceAfter', 'spaceBefore', 'spaceShrinkage', 'splitLongWords',
#       'strikeColor', 'strikeGap', 'strikeOffset', 'strikeWidth', 'textColor', 'textTransform',
#       'underlineColor', 'underlineGap', 'underlineOffset', 'underlineWidth', 'uriWasteReduce', 'wordWrap']
