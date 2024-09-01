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


def process_markdown_files(directory):
    image_folder = os.path.join(directory, "images")
    os.makedirs(image_folder, exist_ok=True)

    pattern = r"\[!\[.*?\]\((.*?)\)\]\((.*?)\)"

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                def replace_image(match):
                    thumbnail_url = match.group(1)
                    full_url = match.group(2)
                    filename = download_image(full_url, image_folder)
                    if filename:
                        return f"![](./images/{filename})"
                    return match.group(0)

                new_content = re.sub(pattern, replace_image, content)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print(f"Processed: {filepath}")


if __name__ == "__main__":
    current_directory = os.getcwd()
    process_markdown_files(current_directory)
