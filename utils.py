import re

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

styles = getSampleStyleSheet()


def bullet_points(points, style=styles["Normal"]):
    bullets = []
    for point in points:
        if isinstance(point, str):
            point = markdown_replace(point)
            bullets.append(Paragraph("<bullet>&bull;</bullet> " + point, style))
        if isinstance(point, list): # for listing certificates
            for subpoint in point:
                subpoint = markdown_replace(subpoint)
                bullets.append(
                    Paragraph(
                        "<bullet>&nbsp;&nbsp;&nbsp;&nbsp;&bull;</bullet> " + subpoint,
                        style,
                    )
                )
    return bullets



def simple_text(text, style=styles["Normal"]):
    bullets = []
    if not text:
        return []
    return [Paragraph(markdown_replace(text), style)]
    for point in points:
        if isinstance(point, str):
            point = markdown_replace(point)
            bullets.append(Paragraph("<bullet>&bull;</bullet> " + point, style))
        if isinstance(point, list): # for listing certificates
            for subpoint in point:
                subpoint = markdown_replace(subpoint)
                bullets.append(
                    Paragraph(
                        "<bullet>&nbsp;&nbsp;&nbsp;&nbsp;&bull;</bullet> " + subpoint,
                        style,
                    )
                )
    return bullets



def _bold(s):
    # s=' '+s
    sp = s.split("**")
    if len(sp) == 1:
        return s
    r = [" <b>", "</b>"]
    i = 0
    result = ""
    result += sp[0]
    for spp in sp[1:]:
        result += r[i]
        i = (i + 1) % 2
        result += spp
    return result


def _line_breaks(s):
    return s.replace('  ','<br></br>')


def link(url, label):
    return f'<a href="{url}"><font color="#0000EE"><u>{label}</u></font></a>'


def _markdown_links(s: str) -> str:
    """
    Converts markdown-style links [text](url)
    into HTML <a> links with a custom style.
    """
    # Use non-greedy matching for both brackets and parentheses
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    def replacer(match):
        text = match.group(1)
        url = match.group(2)
        return f'<a href="{url}"><font color="#213980"><u>{text}</u></font></a>'

    return pattern.sub(replacer, s)


def markdown_replace(s):
    return _markdown_links(_line_breaks(_bold(s)))
