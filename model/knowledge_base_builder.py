import os

import xml.etree.ElementTree as ET

import requests

class KnowledgeBaseBuilder:
    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.dirname(current_path)
        self.assets_path = os.path.join(parent_folder, "assets")
        self.xml_file_name = "darkshampoo-sitemap.xml"


    def extract_urls_from_sitemap(self):
        
        # Get the path of the XML file
        xml_file_path = os.path.join(self.assets_path, self.xml_file_name)
        print(xml_file_path)

        with open(xml_file_path, 'r') as file:
            xml_content = file.read()

        # Parse the XML content
        root = ET.fromstring(xml_content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Find all <loc> elements within the namespace
        urls = [elem.text for elem in root.findall('ns:url/ns:loc', namespace)]
        
        return urls
    
    def save_markdown_from_url(self):
        urls = self.extract_urls_from_sitemap()
        for url in urls:
            markdown_file_name = url.split("/")[-1]+".md"
            url = "https://r.jina.ai/"+url
            markdown_content = requests.get(url).text
            print(markdown_content)

            markdown_file_path = os.path.join(self.assets_path, markdown_file_name)
            with open(markdown_file_path, "w") as file:
                file.write(markdown_content)
            
            print(f"Markdown file saved to {markdown_file_path}")


if __name__ == "__main__":
    kb_builder = KnowledgeBaseBuilder()
    kb_builder.save_markdown_from_url()