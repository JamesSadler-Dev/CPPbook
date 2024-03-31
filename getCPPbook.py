import requests
from bs4 import BeautifulSoup
import re

def main():

    index = requests.get("https://www.learncpp.com").text
    text = BeautifulSoup(index,features="html.parser").select(".lessontable-row-title > a")
    
    links= []
    with open("cppbook.html","w",encoding="utf-8") as file:
        file.write("""
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="style.css">
        </head>
                   """)
        file.write("<body><h1>LearnCPP.com to Book conversion</h1>\n\n<h2>Index:</h2>\n\n<ul>")
        
        for item in text:
            item_text = item.get_text()
            link = item.attrs.get("href","na")

            if link != "na":
                links.append(link)
                file.write(f"<li><a href={link}><big>{item_text}</big></li><br>\n")
        file.write("</ul></a>")

        i = 1
        for link in links:
            page = requests.get(link).text
            parsed = BeautifulSoup(page,features="html.parser").find_all("article")
            
            
            for article in parsed:
                article = str(article).split("\n")
                section_code= f"<hr><a href=cppbook.html#sect{i} name=sect{i} class=sect>Section {i}</a>"
                file.write(section_code)
                i+=1
                for line in article:    

                    if line.startswith("<div class=\"prevnext"):
                        break
                    line = line.strip()
                    if line.startswith("<a"):
                        line = re.sub("</?a.+>","",line)
                    if len(line) > 1:
                        file.write(f"{line}\n")
                    

        file.write("</body>")
                


main()

