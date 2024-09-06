import shutil
import os
from parser_logic import markdown_to_html_node, extract_title

def copy(path, new_path):
    if os.path.isfile(path):
        shutil.copyfile(path, new_path)
    else:
        files = os.listdir(path)
        for file in files:
            path_to_file = os.path.join(path, file)
            path_to_new_file = os.path.join(new_path, file)
            if os.path.isdir(path_to_file) and (not os.path.exists(path_to_new_file)):
                os.mkdir(path_to_new_file)
            copy(path_to_file, path_to_new_file)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        article_text_markdown = f.read()
    with open(template_path, "r") as f:
        template_text = f.read()
    article_text_html = markdown_to_html_node(article_text_markdown).to_html()
    article_title = extract_title(article_text_markdown)
    template_text = template_text.replace("{{ Title }}", article_title).replace("{{ Content }}", article_text_html)
    try:
        os.makedirs(os.path.dirname(dest_path))
    except:
        pass
    with open(dest_path, "w") as f:
        f.write(template_text)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content) and os.path.basename(dir_path_content).endswith(".md"):
        generate_page(dir_path_content, template_path, dest_dir_path.replace(".md",".html"))
    else:
        files = os.listdir(dir_path_content)
        for file in files:
            generate_page_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))

def main():
    if os.path.exists("public/"): shutil.rmtree("public/")
    os.mkdir("public/")
    copy("static/", "public/")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_page_recursive("content/", "template.html", "public/")

if __name__ == "__main__":
    main()