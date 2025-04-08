# utils.py
import re
from datetime import datetime

def convertir_date(pdf_timestamp):
    """Convertit un timestamp PDF en date ISO."""
    date_obj = datetime.strptime(pdf_timestamp[2:10], "%Y%m%d").date()
    return date_obj.isoformat()

def convert_pdf_timestamp_to_iso_date(pdf_timestamp):
    """Convertit un timestamp PDF en date ISO (extraction de la partie YYYYMMDD)."""
    pdf_timestamp = pdf_timestamp[2:]
    timestamp_str = pdf_timestamp[:8]
    date_obj = datetime.strptime(timestamp_str, "%Y%m%d").date()
    return date_obj.isoformat()

def normalize_name(name):
    """Nettoie un nom pour l'utiliser dans un fichier (remplacement des caractères spéciaux)."""
    name = name.lower().strip()
    # \W est un raccourci qui correspond à tout caractère qui n'est pas une lettre, un chiffre ou un underscore (_). 
    # Cela inclut des symboles, des espaces, des ponctuations, etc.
    # \w, qui correspond à des caractères alphanumériques (lettres et chiffres) et le underscore (_).
    name = re.sub(r"\W+", "_", name)
    return name.strip("_")

def extract_title_and_author(title_text):
    """Extrait le titre et l'auteur d'un texte de titre en markdown."""
    author = None
    # groupe de capture ((.+?)) correspond à tout texte avant un espace, un tiret ou une parenthèse ouvrante.
    # groupe de capture ((.*?)) capture le texte suivant ce séparateur jusqu'à une parenthèse fermante éventuelle ou la fin de la ligne.
    match = re.search(r"^(.+?)[\s\-\(](.*?)[\)]?$", title_text)
    
    if match and len(match.groups()) == 2:
        title = match.group(1).strip()
        possible_author = match.group(2).strip()
        # Commence par un mot avec une majuscule suivi de lettres minuscules (cela pourrait être un prénom).
        # Présence d'un second mot après un espace, qui commence également par une majuscule et contient des lettres minuscules (cela pourrait être un nom de famille).
        if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)?$", possible_author):
            author = possible_author
        else:
            title = title_text.strip()
    else:
        title = title_text.strip()
    
    return title, author if author else "inconnu"
