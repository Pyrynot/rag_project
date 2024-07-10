import os
import json
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from dotenv import load_dotenv

load_dotenv()

input_directory = os.getenv('INPUT_DIRECTORY')
output_directory = os.getenv('OUTPUT_DIRECTORY')

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def convert_html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    converter = MarkdownConverter(heading_style="ATX")

    # there are about 20 pages with HTML where colspan=100%, which isn't a valid integer
    """
    # Handle invalid colspan by overriding the conversion process
    for th in soup.find_all('th'):
        colspan = th.get('colspan')
        if colspan and not colspan.isdigit():
            print(f"Invalid colspan '{colspan}' found. Setting to default value of 1.")
            th['colspan'] = '1'
    """

    try:
        markdown_content = converter.convert_soup(soup)
    except ValueError as e:
        raise e
    return markdown_content

def save_markdown_file(markdown_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)

def process_json_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    total_files = len(json_files)
    print(f"Total number of files: {total_files}")

    error_files = []

    for count, json_file in enumerate(json_files):
        json_file_path = os.path.join(input_dir, json_file)
        markdown_file_path = os.path.join(output_dir, f"{os.path.splitext(json_file)[0]}.md")

        if os.path.exists(markdown_file_path):
            print(f"Skipping {json_file} as it is already converted.")
            continue

        try:
            data = read_json_file(json_file_path)
            html_content = data.get("content", "")
            markdown_content = convert_html_to_markdown(html_content)
            save_markdown_file(markdown_content, markdown_file_path)

        except ValueError as e:
            print(f"Error converting {json_file}: {e}")
            error_files.append(json_file)

        if (count + 1) % 20 == 0 or (count + 1) == total_files:
            print(f"{count + 1} / {total_files} converted")

    if error_files:
        print("\nFiles with conversion errors:")
        for error_file in error_files:
            print(error_file)

if __name__ == "__main__":
    process_json_files(input_directory, output_directory)