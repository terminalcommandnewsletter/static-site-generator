from textnode import *
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    escaped_delimiter = delimiter.replace("*","\\*")
    for node in old_nodes:
        # if node.text_type != "text": continue
        # token = ""
        # last_character = 0
        # in_type_block = False
        # for char in range(len(node.text)):
            # if node.text[char] == delimiter[0]:
            #     if (char - last_character) > len(delimiter): 
            #         in_type_block = not in_type_block
            #         if in_type_block == False:
            #             new_nodes.append(TextNode(token, text_type, None))
            #         else:
            #             new_nodes.append(TextNode(token, "text", None))
            #         token = ""
            #     last_character = char
            #     continue
            # token += node.text[char]
        appended = False
        if node.text_type == "text":
            extracted = re.findall(fr"{escaped_delimiter}(.*?){escaped_delimiter}", node.text)
            start_pos = 0
            for i in extracted:
                ind = node.text.index(f"{delimiter}{i}{delimiter}")
                new_nodes.append(TextNode(node.text[start_pos:ind],"text"))
                new_nodes.append(TextNode(f"{i}",text_type))
                # appended = True
                start_pos = ind + len(f"{delimiter}{i}{delimiter}")
                # if in_type_block == False:
                #     new_nodes.append(TextNode(token, text_type, None))
                # else:
                #     new_nodes.append(TextNode(token, "text", None))
            new_nodes.append(TextNode(node.text[start_pos:],"text"))
        else: new_nodes.append(TextNode(node.text, node.text_type, node.url))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    start_pos = 0
    for node in old_nodes:
        appended = False
        if node.text_type == "text":
            extracted = extract_markdown_images(node.text)
            if extracted:
                for i in extracted:
                    match_index = node.text.index(f"![{i[0]}]({i[1]})")
                    new_nodes.append(TextNode(node.text[start_pos:match_index], "text"))
                    new_nodes.append(TextNode(i[0], "image", i[1]))
                    appended = True
                    start_pos = match_index + len(f"![{i[0]}]({i[1]})")
                if start_pos < len(node.text): new_nodes.append(TextNode(node.text[start_pos:], "text"))
        if not appended: new_nodes.append(node)
    if new_nodes == []: new_nodes = old_nodes.copy()
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    start_pos = 0
    for node in old_nodes:
        appended = False
        if node.text_type == "text":
            extracted = extract_markdown_links(node.text)
            if extracted:
                for i in extracted:
                    match_index = node.text.index(f"[{i[0]}]({i[1]})")
                    new_nodes.append(TextNode(node.text[start_pos:match_index], "text"))
                    new_nodes.append(TextNode(i[0], "link", i[1]))
                    appended = True
                    start_pos = match_index + len(f"[{i[0]}]({i[1]})")
                if start_pos < len(node.text): new_nodes.append(TextNode(node.text[start_pos:], "text"))
        if not appended: new_nodes.append(node)
    if new_nodes == []: new_nodes = old_nodes.copy()
    return new_nodes

def text_to_textnodes(text):
    # return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text,"text")],"**","bold"),"*","italic"),"`","code")))
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    return list(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, markdown.split("\n\n"))))

def block_to_block_type(markdown):
    if re.match(r"^[#]{6} ", markdown): return "heading-6"
    if re.match(r"^[#]{5} ", markdown): return "heading-5"
    if re.match(r"^[#]{4} ", markdown): return "heading-4"
    if re.match(r"^[#]{3} ", markdown): return "heading-3"
    if re.match(r"^[#]{2} ", markdown): return "heading-2"
    if re.match(r"^[#]{1} ", markdown): return "heading-1"
    if re.match(r"^```(.|\n)*?```", markdown): return "code"
    if re.match(r"^> ", markdown): return "quote"
    if re.match(r"^[*-] ", markdown): return "unordered-list"
    if re.match(r"^\d+\. ", markdown): return "ordered-list"
    return "normal-paragraph"

## Final parsing

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = None
        if "heading-" in block_type:
            node = ParentNode(tag=f"h{block_type[8:]}", children=map(text_node_to_html_node, text_to_textnodes(block.lstrip("# "))))
        elif block_type == "code":
            node = ParentNode(tag="pre", children=[LeafNode(tag="code", value=block.strip("```").strip("\n"))])
        elif block_type == "quote":
            node = ParentNode(tag="blockquote", children=map(text_node_to_html_node, text_to_textnodes(block.lstrip("> "))))
        elif block_type == "unordered-list":
            node = ParentNode(tag="ul", children=list(map(lambda x: ParentNode(tag="li", children=map(text_node_to_html_node, text_to_textnodes(x.lstrip("* ").lstrip("- ")))), block.split("\n"))))
        elif block_type == "ordered-list":
            node = ParentNode(tag="ol", children=list(map(lambda x: ParentNode(tag="li", children=map(text_node_to_html_node, text_to_textnodes(x.replace(re.match(r"^(\d+\. )", x).group(), "")))), block.split("\n"))))
        elif block_type == "normal-paragraph":
            node = ParentNode(tag="p", children=map(text_node_to_html_node, text_to_textnodes(block)))
        # node.text = 
        nodes.append(node)
    return ParentNode(nodes,"div")

def extract_title(markdown):
    heading = list(filter(lambda x: block_to_block_type(x) == "heading-1", markdown_to_blocks(markdown)))
    if heading is []:
        raise Exception("No heading")
    return heading[0][2:].strip()