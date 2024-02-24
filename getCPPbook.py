import requests
from bs4 import BeautifulSoup

def main():

    months = {
              "JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY"
              "AUGUST", "SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER" 
             }

    index = requests.get("https://www.learncpp.com").text
    text = BeautifulSoup(index,features="html.parser").select(".lessontable-row-title > a")

    links= []
    with open("cppbook.md","w",encoding="utf-8") as file:
        file.write("<h1>LearnCPP.com to Book conversion</h1>\n\n<h2>Index:</h2>\n\n<ul>")
        
        for item in text:
            item_text = item.get_text()
            link = item.attrs.get("href","na")

            if link != "na":
                links.append({item_text:link})
                file.write(f"<li><a href={link}><big>{item_text}</big></li><br>\n")
        file.write("</ul></a>")

        for dictionary in links:
            for item_text,link in dictionary.items():
                page = requests.get(link).text
                parsed = BeautifulSoup(page,features="html.parser").find("article").children
                file.write(f"<h2>{item_text}</h2>\n")

                for child in parsed:
                    child_text = child.get_text().splitlines()
                    
                    for line in child_text:

                        if line.split(" ")[0].upper().strip() in months or len(line.split(" ")) == 1:
                            continue
                        elif line.upper() == "NEXT LESSON":
                            break
                        else:
                            file.write(f"{line}\n")
                    file.write("\n")
                

main()

