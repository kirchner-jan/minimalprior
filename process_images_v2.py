import os
import re
import requests
import string
import uuid
from urllib.parse import urlparse
from pathlib import Path


def clean_filename(filename):
    # Remove the file extension
    name, ext = os.path.splitext(filename)

    # Replace spaces with underscores and remove non-alphanumeric characters
    clean_name = re.sub(r"[^\w\-_]", "", name.replace(" ", "_"))

    # If the filename becomes empty after cleaning, use a UUID
    if not clean_name:
        clean_name = str(uuid.uuid4())

    # Truncate to a reasonable length and add back the extension
    return clean_name[:50] + ext


def download_image(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        original_filename = os.path.basename(urlparse(url).path)
        clean_name = clean_filename(original_filename)
        filepath = os.path.join(folder, clean_name)

        # Handle potential filename conflicts
        counter = 1
        while os.path.exists(filepath):
            name, ext = os.path.splitext(clean_name)
            filepath = os.path.join(folder, f"{name}_{counter}{ext}")
            counter += 1

        with open(filepath, "wb") as f:
            f.write(response.content)
        return os.path.basename(filepath)
    return None


def process_markdown_file(filepath):
    image_folder = os.path.join(os.path.dirname(filepath), "images")
    os.makedirs(image_folder, exist_ok=True)

    pattern = r"!\[.*?\]\((.*?)\)"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    def replace_image(match):
        full_url = match.group(1)
        filename = download_image(full_url, image_folder)
        if filename:
            return f"![](./images/{filename})"
        return match.group(0)

    new_content = re.sub(pattern, replace_image, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Processed: {filepath}")


if __name__ == "__main__":
    if len(os.sys.argv) != 2:
        print("Usage: python process_images_v2.py <markdown_file_path>")
        os.sys.exit(1)

    markdown_file_path = os.sys.argv[1]
    if not os.path.isfile(markdown_file_path):
        print(f"Error: File '{markdown_file_path}' not found.")
        os.sys.exit(1)

    process_markdown_file(markdown_file_path)
