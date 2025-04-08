# pdf_processing.py
import os
import fitz  # PyMuPDF
import pymupdf4llm
import json
from utils import normalize_name, extract_title_and_author, convert_pdf_timestamp_to_iso_date
import re

def traiter_pdf(pfichier, input_folder, output_folder):
    """Traite un fichier PDF et extrait les articles sous forme de fichiers JSON."""
    try:
        pdf_file = os.path.join(input_folder, pfichier)
        doc = fitz.open(pdf_file)
        print(f"Fichier traité : {pfichier}")
        print(f"Nombre de pages : {len(doc)}")
        print('output',output_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        articles = []
        current_article = None

        for page_num in range(1,len(doc)):
            print(f"🔹 Traitement de la page {page_num}...")
            page_md = pymupdf4llm.to_markdown(doc, pages=[page_num], margins=(0, 0, 0, 35)).strip()
            # Commence par un # suivi de zéro ou plusieurs espaces, puis tout texte après. 
            # groupe (.+) n'importe quel caractère sauf les sauts de ligne/une ou plusieurs occcurences
            # Titre du document.
            title_match = re.search(r"^#\s*(.+)", page_md)

            if title_match:
                raw_title = title_match.group(1).strip()
                title, author = extract_title_and_author(raw_title)
                #if author == 'inconnu':
                #   author = None


                print(f"📌 Titre détecté : {title}")
                print(f"✍ Auteur détecté : {author}")

                if current_article:
                    articles.append(current_article)
                
                current_article = {
                    "title": title,
                    "author": author,
                    "pages": [page_num + 1],
                    "content": [page_md]
                }
            else:
                if current_article:
                    current_article["pages"].append(page_num + 1)
                    current_article["content"].append(page_md)

        if current_article:
            articles.append(current_article)

        for article in articles:
            first_page = article["pages"][0]
            last_page = article["pages"][-1]
            nom_fichier, _ = os.path.splitext(pfichier)
            file_name = f"{nom_fichier}_{first_page}_{last_page}.json"
            file_path = os.path.join(output_folder, file_name)

            clean_text = "".join(article["content"])
            article["title"] = article["title"].replace('#####','').replace('*','').strip()
            article["author"] = article["author"].replace('#####','').replace('inconnu','').strip()
            
            if len(article["title"]) > 100:
                article["title"] = ""

            article_data = {
                "metadata": {
                    "title": article["title"],
                    "authors": article["author"],
                    "creationDate": convert_pdf_timestamp_to_iso_date(doc.metadata["creationDate"]),
                    "originalFile": pfichier,
                    "pages": article["pages"],
                },
                "text": clean_text
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(article_data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Erreur lors du traitement du fichier {pfichier}: {e}")

def traiter_repertoire(repertoire, output_folder):
    """Traite tous les fichiers PDF d'un répertoire donné."""
    if not os.path.exists(repertoire):
        print(f"Le répertoire {repertoire} n'existe pas.")
        return
    for fichier in os.listdir(repertoire):
        fichier_path = os.path.join(repertoire, fichier)
        if os.path.isfile(fichier_path) and fichier.lower().endswith('.pdf'):
            traiter_pdf(fichier, repertoire, output_folder)
        
