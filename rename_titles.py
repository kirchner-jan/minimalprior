import re
import os


def remove_colons(text):
    return text.replace(":", "")


def update_markdown_files(input_file):
    with open(input_file, "r") as f:
        content = f.read()

    # Regular expression to find links and descriptions
    pattern = r"\[(.*?)\]\((.*?)\.html\)\s*(.*)"
    matches = re.findall(pattern, content)

    for title, path, description in matches:
        md_file = path.replace("./posts/", "./posts/") + ".md"
        if not os.path.exists(md_file):
            print(f"Warning: {md_file} does not exist. Skipping.")
            continue

        with open(md_file, "r") as f:
            md_content = f.read()

        # Remove colons from title and description
        title_no_colon = remove_colons(title)
        description_no_colon = remove_colons(description)

        # Update title
        md_content = re.sub(r"title:.*", f"title: {title_no_colon}", md_content)

        # Update subtitle
        md_content = re.sub(
            r"subtitle:.*", f"subtitle: {description_no_colon}", md_content
        )

        with open(md_file, "w") as f:
            f.write(md_content)

        print(f"Updated {md_file}")


# Usage
input_file = "index.md"
update_markdown_files(input_file)
