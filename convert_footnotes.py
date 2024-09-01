import os
import re


def convert_footnotes(content):
    # Find all footnote references in the text
    reference_pattern = r"\[(\d+)\]\(.*?#footnote-\d+-\d+\)"
    references = re.findall(reference_pattern, content)

    # Find all footnote definitions
    definition_pattern = r"\[(\d+)\]\(.*?#footnote-anchor-\d+-\d+\)\n(.*?)(?=\n\n|\[|$)"
    definitions = re.findall(definition_pattern, content, re.DOTALL)

    # Create a dictionary to store footnote content
    footnotes = {num: text.strip() for num, text in definitions}

    # Replace footnote references
    for num in references:
        old_ref = f"[{num}](https://universalprior.substack.com/p/this-week-in-fashion#footnote-{num}-\d+)"
        new_ref = f"[^{num}]"
        content = re.sub(old_ref, new_ref, content)

    # Remove old footnote definitions
    content = re.sub(definition_pattern, "", content, flags=re.DOTALL)

    # Add new footnote definitions at the end of the content
    content += "\n\n"
    for num, text in footnotes.items():
        content += f"[^{num}]: {text}\n"

    return content


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            new_content = convert_footnotes(content)

            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_content)

            print(f"Processed: {filename}")


# Usage
directory = "./posts/universalprior"  # Current directory
process_directory(directory)
