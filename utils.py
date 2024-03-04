import re
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def bullet_points(points, style=styles["Normal"]):
    bullets = []
    for point in points:
        if isinstance(point, str):
            point = markdown_replace(point)
            bullets.append(Paragraph("<bullet>&bull;</bullet> " + point, style))
        if isinstance(point, list):
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

    # print("--",result)
    return result


def _markdown_links(s):
    print(s)
    site = re.compile("\[(.*)\]").search(s)
    url = re.compile("\((.*)\)").search(s)

    # "aaaa [Full list on LinkedIn](https://www.linkedin.com/in/scheuclu)"
    # "aaa  <a href='TODO'> word </a>

    if site is not None and url is not None:
        print(site.group(1), url.group(1))
        # return s
        s = s.replace(
            f"[{site.group(1)}]({url.group(1)})",
            f"<a href='{url.group(1)})'> {site.group(1)} </a>",
        )

    return s


def markdown_replace(s):
    return _markdown_links(_bold(s))
