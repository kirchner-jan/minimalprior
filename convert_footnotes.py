import os
import re

# \(https://universalprior\.substack\.com/p/[^#\)]+#footnote[^)]+\)
# find ./posts/universalprior -name "*.md" | while read -r file; do     echo "Processing $file"
#     sed -i -E ':a;N;$!ba;s/\n\n\[([0-9]+)\]\n\n/\n\n[^\1]:/g' "$file"; done

# find ./posts/universalprior -name "*.md" | xargs sed -i -E 's/\[([0-9]+)\]/[^\1]/g'


def convert_footnotes(content):
    # Find all footnote references and definitions
    pattern = r"\[(\d+)\]\((.*?#footnote-\d+-\d+)\).*?\n\[(\d+)\]\((.*?#footnote-anchor-\d+-\d+)\)\n(.*?)(?=\n\n|\[|$)"
    matches = list(re.finditer(pattern, content, re.DOTALL))

    # Process matches in reverse order to avoid messing up indices
    for match in reversed(matches):
        ref_num, ref_url, def_num, def_url, footnote_text = match.groups()
        if ref_num == def_num:
            # Replace the entire match with the new format
            new_footnote = f"[^{ref_num}]\n\n[^{ref_num}]: {footnote_text.strip()}\n\n"
            content = content[: match.start()] + new_footnote + content[match.end() :]

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
directory = "./posts/universalprior"
if os.path.exists(directory):
    process_directory(directory)
else:
    print(f"Error: The directory {directory} does not exist.")
