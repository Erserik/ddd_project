import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_report_pdf(post):
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    file_path = os.path.join(reports_dir, f"report_{post.sha256_hash}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Заголовок
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)
    c.drawString(50, height - 60, "Document Authenticity Report")

    # Данные
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(50, height - 110, f"Title: {post.title}")
    c.drawString(50, height - 140, f"User: {post.user.username}")
    c.drawString(50, height - 170, f"Status: {post.status.capitalize()}")
    c.drawString(50, height - 200, f"Similarity: {round(post.similarity_score * 100, 2)}%")
    c.drawString(50, height - 230, "SHA256 Hash:")
    c.setFont("Courier", 10)
    c.drawString(50, height - 250, post.sha256_hash)

    # График похожести
    bar_width = 300
    similarity_bar = post.similarity_score * bar_width
    c.setFillColor(colors.grey)
    c.rect(50, height - 290, bar_width, 15, fill=0)
    c.setFillColor(colors.green)
    c.rect(50, height - 290, similarity_bar, 15, fill=1)

    # Подвал
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.darkgray)
    c.drawString(50, 30, "Generated automatically by the system")

    c.save()
