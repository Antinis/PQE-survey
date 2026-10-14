"""Export this figure's editable SVG primitives to an embedded-font vector PDF.

Usage: python figures/render_attention_comparison.py
Supported elements are deliberately limited to those used by this SVG.
"""

from pathlib import Path
import xml.etree.ElementTree as ET

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def render():
    source = Path(__file__).with_name("attention-cache-sharing.svg")
    target = source.with_suffix(".pdf")
    root = ET.parse(source).getroot()
    width, height = map(float, (root.attrib["width"], root.attrib["height"]))
    fonts = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("FigureArial", str(fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("FigureArialBold", str(fonts / "arialbd.ttf")))
    doc = canvas.Canvas(str(target), pagesize=(width, height), pageCompression=1)
    doc.setTitle("KV-cache sharing in MHA, GQA, MQA, and CLA")
    doc.setSubject("Two adjacent layers with four independent query heads per layer")

    for element in root:
        tag = element.tag.rsplit("}", 1)[-1]
        attrs = element.attrib
        if tag in ("title", "desc"):
            continue
        stroke = attrs.get("stroke", "none")
        fill = attrs.get("fill", "none")
        if stroke != "none":
            doc.setStrokeColor(HexColor(stroke))
        if fill != "none":
            doc.setFillColor(HexColor(fill))
        doc.setLineWidth(float(attrs.get("stroke-width", 1)))
        if tag == "rect":
            x, y, w, h = (float(attrs[k]) for k in ("x", "y", "width", "height"))
            radius = float(attrs.get("rx", 0))
            if radius:
                doc.roundRect(x, height - y - h, w, h, radius,
                              stroke=int(stroke != "none"), fill=int(fill != "none"))
            else:
                doc.rect(x, height - y - h, w, h,
                         stroke=int(stroke != "none"), fill=int(fill != "none"))
        elif tag == "line":
            x1, y1, x2, y2 = (float(attrs[k]) for k in ("x1", "y1", "x2", "y2"))
            doc.line(x1, height - y1, x2, height - y2)
        elif tag == "text":
            font = "FigureArialBold" if attrs.get("font-weight") == "bold" else "FigureArial"
            doc.setFont(font, float(attrs.get("font-size", 22)))
            x, y = float(attrs["x"]), height - float(attrs["y"])
            content = "".join(element.itertext())
            anchor = attrs.get("text-anchor", "start")
            if anchor == "middle":
                doc.drawCentredString(x, y, content)
            elif anchor == "end":
                doc.drawRightString(x, y, content)
            else:
                doc.drawString(x, y, content)
        else:
            raise ValueError(f"Unsupported SVG element: {tag}")

    doc.showPage()
    doc.save()
    print(f"Vector figure saved: {target}")


if __name__ == "__main__":
    render()
