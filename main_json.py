# main.py
from pdf_processing import traiter_repertoire

def main():
    input_folder = "input"
    output_folder = "docs"
    traiter_repertoire(input_folder, output_folder)

if __name__ == "__main__":
    main()