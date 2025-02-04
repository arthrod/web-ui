#!/usr/bin/env python3

import sys
import os
from bs4 import BeautifulSoup


def extract_external_js(html_content):
    """
    Parse the HTML content and return a list of external JavaScript URLs (script src).
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    external_scripts = []
    for script in soup.find_all('script'):
        src = script.get('src')
        if src:
            external_scripts.append(src)

    return external_scripts


def dom_main(html_file_path, output_file_path):
    """
    Main function:
      - Reads HTML from the specified file
      - Extracts external <script src=...">
      - Writes each src into a text file (one per line)
    """

    if not os.path.isfile(html_file_path):
        print(f"Error: File '{html_file_path}' does not exist.")
        sys.exit(1)

    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    external_scripts = extract_external_js(html_content)

    # Write external script URLs to a txt file
    with open(output_file_path, 'w', encoding='utf-8') as out:
        for src in external_scripts:
            out.write(src + "\n")

    print(f"Extracted {len(external_scripts)} external scripts and saved to '{output_file_path}'.")


if __name__ == "__main__":
    # Modify these paths as needed
    html_file_path = "final_dom.html"
    output_file_path = "external_scripts.txt"
    dom_main(html_file_path, output_file_path)
