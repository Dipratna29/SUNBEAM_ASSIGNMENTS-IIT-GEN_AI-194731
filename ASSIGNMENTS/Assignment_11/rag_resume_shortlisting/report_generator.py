from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(filename, summary, score_details):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>AI Resume Evaluation Report</b>", styles["Title"]))
    content.append(Paragraph("<br/>", styles["Normal"]))

    content.append(Paragraph("<b>Professional Summary</b>", styles["Heading2"]))
    content.append(Paragraph(summary, styles["Normal"]))

    content.append(Paragraph("<br/>", styles["Normal"]))
    content.append(Paragraph("<b>Resume Evaluation</b>", styles["Heading2"]))
    content.append(Paragraph(score_details.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(content)