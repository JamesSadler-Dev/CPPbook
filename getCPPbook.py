import requests
from bs4 import BeautifulSoup
import re

def write_head_tag(file):
            file.write("""
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
        """)
            
def write_header(file,page):
        file.write(f"""
            <div class=headerbar>
                <h1>LearnCPP.com to Book Conversion</h1>
                <span> Page {page} </span>
            </div>
            <main>
                <a href=tableofcontents.html target=_blank class=tableofcontents>
                <h2>Table of Contents</h2></a><br>
            """)

def write_closing_tags(file):
     file.write("</main></body>")
     file.close()


def check_fix_and_write_lines(article,file):
    for line in article:    
        if line.startswith("<div class=\"prevnext"):
            break
        if line.startswith("<a"):
            line = re.sub("</?a.+>","",line)
        file.write(f"{line}\n")
        

def main():
    index = requests.get("https://www.learncpp.com").text
    text = BeautifulSoup(index,features="html.parser").select(".lessontable-row-title > a")
    page_num = 1
    links= []
    current_link = f"cppbook-pg{page_num}.html"
    with open(current_link,"w",encoding="utf-8") as file:
        write_head_tag(file)
        write_header(file,page_num)
    
    with open("tableofcontents.html","w",encoding="utf-8") as file:
        write_head_tag(file)
        file.write("<h1>CPP Book Table of contents </h1><a href=\"./cppbook-pg1.html\">To Book</a><hr><ul>")
        for item in text:
            item_text = item.get_text()
            link = item.attrs.get("href","na")

            if link != "na":
                links.append(link)
                file.write(f"<li><a href={link}><big>{item_text}</big></li><br>\n")
        file.write("</ul></a></body>")

        file = open(current_link,"a",encoding="utf-8")

        i = 1
        for link in links:
            page = requests.get(link).text
            parsed = BeautifulSoup(page,features="html.parser").find("article")
            
            article = str(parsed).split("\n")
            section_code= f"<hr><a href={current_link}#sect{i} name=sect{i} class=sect>Section {i}</a>"
            file.write(section_code)
            i+=1
            
            check_fix_and_write_lines(article,file)

            if i % 100 == 0:
                page_num+=1
                current_link= f"cppbook-pg{page_num}.html"
                if page_num == 2:
                    file.write(f"""
                        <hr>
                        <div class=footer>
                            <a href={current_link}> <h2>Next Page</h2> </a>
                        </div>
                        """)
                else:
                      prev_link = f"cppbook-pg{page_num - 1}.html"
                      file.write(f"""
                        <hr>
                        <div class=footer>
                            <a href={prev_link}><h2>Previous Page</h2></a>
                            <a href={current_link}><h2>Next Page</h2></a>
                        </div>
                        """)
                      
                write_closing_tags(file)
                file = open(current_link,"w",encoding="utf-8")
                write_head_tag(file)
                write_header(file,page_num)


        write_closing_tags(file)
                
        
                

if __name__ == "__main__":
    main()

