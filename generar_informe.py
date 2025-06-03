from jinja2 import Template
import pdfkit
import datetime
import os


# Ruta del archivo index.html
folder = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(folder, "index.html")

# Leer el contenido original del index.html
with open(html_path, "r", encoding="utf-8") as f:
    original_html = f.read()


# Configuración de pdfkit con ruta de wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Cambiar según tu ruta
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Opciones para permitir acceso local a imágenes y recursos
options = {
    'enable-local-file-access': None
}

# Generar PDF
pdf_output_path = os.path.join(folder, "informe_final.pdf")
pdfkit.from_file(html_path, pdf_output_path, options=options, configuration=config)

print(f"PDF generado correctamente en: {pdf_output_path}")
