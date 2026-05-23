import os
import sys
import markdown
from xhtml2pdf import pisa

def convert_md_to_pdf(md_path, pdf_path):
    if not os.path.exists(md_path):
        print(f"Erro: O arquivo de entrada '{md_path}' nao existe.")
        return False
        
    print(f"Lendo '{md_path}'...")
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Converter markdown para HTML
    print("Convertendo Markdown para HTML...")
    html_content = markdown.markdown(text, extensions=['fenced_code', 'tables'])

    # Template HTML com estilos limpos e profissionais
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: a4;
                margin: 2.5cm 2cm 2.5cm 2cm;
            }}
            body {{
                font-family: Helvetica, Arial, sans-serif;
                color: #2d3748;
                font-size: 10.5pt;
                line-height: 1.6;
            }}
            h1 {{
                font-size: 22pt;
                color: #1a365d;
                margin-top: 0px;
                margin-bottom: 20px;
                padding-bottom: 8px;
                border-bottom: 2px solid #2b6cb0;
            }}
            h2 {{
                font-size: 14pt;
                color: #2b6cb0;
                margin-top: 25px;
                margin-bottom: 10px;
                border-bottom: 1px solid #e2e8f0;
                padding-bottom: 4px;
            }}
            h3 {{
                font-size: 11pt;
                color: #2d3748;
                margin-top: 15px;
                margin-bottom: 5px;
                font-weight: bold;
            }}
            p {{
                margin-bottom: 12px;
                text-align: justify;
            }}
            ul, ol {{
                margin-left: 20px;
                margin-bottom: 12px;
            }}
            li {{
                margin-bottom: 6px;
            }}
            code {{
                font-family: Courier, monospace;
                background-color: #f7fafc;
                color: #c53030;
                padding: 1px 3px;
                font-size: 9pt;
            }}
            pre {{
                background-color: #f7fafc;
                border: 1px solid #e2e8f0;
                padding: 10px;
                margin-bottom: 15px;
                font-family: Courier, monospace;
                font-size: 8.5pt;
            }}
            pre code {{
                color: #2d3748;
                background-color: transparent;
                padding: 0;
            }}
            hr {{
                border: 0;
                border-top: 1px solid #e2e8f0;
                margin-top: 25px;
                margin-bottom: 25px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 15px;
            }}
            th, td {{
                border: 1px solid #e2e8f0;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #edf2f7;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    print(f"Gerando PDF em '{pdf_path}'...")
    with open(pdf_path, 'wb') as f:
        pisa_status = pisa.CreatePDF(html_template, dest=f)
    
    return pisa_status.err == 0

def main():
    # Uso padrao ou argumentos CLI
    if len(sys.argv) == 3:
        md_file = sys.argv[1]
        pdf_file = sys.argv[2]
    else:
        # Valores padrao se nao houver argumentos
        md_file = ".planning/phases/02-resolucao-direcao-motores/PROPOSTA_FASE_2.md"
        pdf_file = "docs/PROPOSTA_FASE_2.pdf"
        print(f"Uso: python docs/convert.py <arquivo.md> <arquivo.pdf>")
        print(f"Usando definicoes padrao...")

    success = convert_md_to_pdf(md_file, pdf_file)
    if success:
        print("PDF gerado com sucesso!")
    else:
        print("Erro ao gerar o PDF!")

if __name__ == "__main__":
    main()
