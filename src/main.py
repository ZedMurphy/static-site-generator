import os
import shutil

from copystatic import copy_files_recursive
from markdowntonode import markdown_to_html_node


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page("content/index.md", "template.html", "public/index.html")

def extract_title(markdown):
    single_lines = markdown.split("\n")
    extracted_title = ""
    for line in single_lines:
        if line.startswith("# "):
            extracted_title = line.lstrip("# ").rstrip()
            break
    if extracted_title == "":
        raise Exception("No site title (h1) found.")
    return extracted_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    # opened_markdown = open(from_path)
    # read_markdown = opened_markdown.read()
    # opened_markdown.close()
    # opened_template = open(template_path)
    # read_template = opened_template.read()
    # opened_template.close()
    with open(from_path, 'r') as f:
        read_markdown = f.read()
    with open(template_path, 'r') as f:
        read_template = f.read()
    
    markdown_as_html_node = markdown_to_html_node(read_markdown)
    markdown_as_html = markdown_as_html_node.to_html()
    
    page_title = extract_title(read_markdown)
    
    title_added = read_template.replace("{{ Title }}", page_title)
    new_page = title_added.replace("{{ Content }}", markdown_as_html)

    dir_names = os.path.dirname(dest_path)
    os.makedirs(dir_names, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(new_page)
        

main()