import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures


def get_head_tag()->str:
            return """
        {% extends "template.html" %}
        """
            
def get_header(page)->str:
        return f"""
            {{% block header %}}
            <div class=headerbar>
                <h1>LearnCPP.com to Book Conversion</h1>
                <span> Section {page} </span>
            </div>
            {{% block body %}}
            <main>
                <a href=tableofcontents.html target=_blank class=tableofcontents>
                <h2>Table of Contents</h2></a><br>
            """

def get_closing_tags()->str:
     return """{% endblock %}</main></body>"""


def get_fixed_lines(article)->list[str]:
    result = []
    for line in article:    
        if line.startswith("<div class=\"prevnext"):
            break
        if line.startswith("<a"):
            line = re.sub("</?a.+>","",line)
        result.append(f"{line}\n")
    return result

        
def get_table_of_contents_and_links(text):
    result = {"text":[],"links":[]}
    result["text"].append(get_head_tag())
    result["text"].append("""
                   {% block header %}
                   <div class=headerbar>
                   <h1>CPP Book Table of contents </h1>
                   </div>
                   <br>
                   <a href="cppbook-pg1.html" style="font-size:larger; font-weight:bold; margin-left:1rem;">To Book</a>
                   <hr>
                   {% endblock %}
                   {% block body %}
                   <ul style="display:flex; flex-direction:column; justify-items:center;">
                   """)
    page= 1
    for num,item in enumerate(text):
        item_text = item.get_text()
        link = item.attrs.get("href","na")
        if link != "na":
            result["links"].append(link)
            if num % 50 == 0:
                    result["text"].append(f"""
                            <li>
                                <h2><a href="cppbook-pg{page}.html" style="font-weight:bolder; font-size:2rem;">
                                Section {page}
                                </a></h2>
                            </li>
                            """)
                    page+=1

            result["text"].append(f"""<li>
                        <span style="font-weight:bold; font-size:larger;">{num+1}. </span>
                        <big>{item_text}</big>
                        </li>
                        <br>\n""")
    result["text"].append("</ul></a>{% endblock%}")
    return result

def get_article(link):
    page = requests.get(link).text
    parsed = BeautifulSoup(page,features="html.parser").find("article")
    article = str(parsed).split("\n")
    return article
    
    
def main():
    index = requests.get("https://www.learncpp.com").text
    text = BeautifulSoup(index,features="html.parser").select(".lessontable-row-title > a")
    page_num = 1
    table_contents_and_links = get_table_of_contents_and_links(text)
    links = table_contents_and_links["links"]

    with open("templates/tableofcontents.html","w",encoding="utf-8") as file:
        file.writelines(table_contents_and_links["text"])

  
if __name__ == "__main__":
    main()


