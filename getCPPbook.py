import requests
from bs4 import BeautifulSoup
import re

def get_head_tag():
            return """
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
        """
            
def get_header(page):
        return f"""
            <div class=headerbar>
                <h1>LearnCPP.com to Book Conversion</h1>
                <span> Section {page} </span>
            </div>
            <main>
                <a href=tableofcontents.html target=_blank class=tableofcontents>
                <h2>Table of Contents</h2></a><br>
            """

def get_closing_tags():
     return """</main></body>"""



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

    with open("tableofcontents.html","w",encoding="utf-8") as file:
        file.write(get_head_tag())
        file.write("""
                   <div class=headerbar>
                   <h1>CPP Book Table of contents </h1>
                   </div>
                   <br>
                   <a href=\"./cppbook-pg1.html\" style="font-size:larger; font-weight:bold; margin-left:1rem;">To Book</a>
                   <hr>
                   <ul style="display:flex; flex-direction:column; justify-items:center;">
                   """)
        
        page= 1
        for num,item in enumerate(text):
            item_text = item.get_text()
            link = item.attrs.get("href","na")
            if link != "na":
                links.append(link)
                if num % 50 == 0:
                     file.write(f"""
                                <li>
                                    <h2><a href="cppbook-pg{page}.html" style="font-weight:bolder; font-size:2rem;">
                                    Section {page}
                                    </a></h2>
                                </li>
                                """)
                     page+=1

                file.write(f"""<li>
                            <span style="font-weight:bold; font-size:larger;">{num+1}. </span>
                            <big>{item_text}</big>
                           </li>
                           <br>\n""")
        file.write("</ul></a></body>")

    current_link = f"cppbook-pg{page_num}.html"
    with open(current_link,"w",encoding="utf-8") as file:
        file.write(get_head_tag())
        file.write(get_header(page_num))

    file = open(current_link,"a",encoding="utf-8")
    i = 1
    for link in links:
        page = requests.get(link).text
        parsed = BeautifulSoup(page,features="html.parser").find("article")
        article = str(parsed).split("\n")
        section_code= f"<hr><a href={current_link}#lesson{i} name=lesson{i} class=sect>Lesson {i}</a>"
        file.write(section_code)
        i+=1
        
        check_fix_and_write_lines(article,file)

        if i % 50 == 0:
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
                    prev_link = f"cppbook-pg{page_num - 2}.html"
                    file.write(f"""
                    <hr>
                    <div class=footer>
                        <a href={prev_link}><h2>Previous Page</h2></a>
                        <a href={current_link}><h2>Next Page</h2></a>
                    </div>
                    """)            
            file.write(get_closing_tags())
            file.close()
            file = open(current_link,"w",encoding="utf-8")
            file.write(get_head_tag())
            file.write(get_header(page_num))

    file.write(get_closing_tags())
    file.close()
                
        
                

if __name__ == "__main__":
    main()

