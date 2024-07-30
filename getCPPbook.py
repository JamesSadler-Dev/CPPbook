import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures

class BookMaker:
    CLOSING_TAG = """{% endblock %}"""
    OPENING_TAG = """{% extends "template.html" %}"""

    
    @staticmethod         
    def get_header(page)->str:
            return f"""
                {{% block header %}}
                <div class=headerbar>
                    <h1>LearnCPP.com to Book Conversion</h1>
                    <span> Section {page} </span>
                </div>
                {{% endblock %}}
                {{% block body %}}
                <main>
                    <a href=/ target=_blank class=tableofcontents>
                    <h2>Table of Contents</h2></a><br>
                """
    
    @staticmethod
    def write_tags(file,tags:str | list[str])->str:
        file.writelines(tags)

    @staticmethod
    def get_fixed_lines(article)->list[str]:
        result = []
        for line in article:    
            if line.startswith("<div class=\"prevnext"):
                break
            if line.startswith("<a"):
                line = re.sub("</?a.+>","",line)
            result.append(f"{line}\n")
        return result

    @staticmethod        
    def get_table_of_contents_and_links(text)->dict[str,list[str]]:
        result = {"text":[],"links":[]}
        result["text"].append(BookMaker.get_head_tag())
        result["text"].append("""
                    {% block header %}
                    <div class=headerbar>
                    <h1>CPP Book Table of contents </h1>
                    </div>
                    <br>
                    <a href="cppbook-pg1" style="font-size:larger; font-weight:bold; margin-left:1rem;">To Book</a>
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
                                    <h2><a href="cppbook-pg{page}" style="font-weight:bolder; font-size:2rem;">
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

    @staticmethod
    def get_article(link:str)->list[str]:
        page:str = requests.get(link).text
        parsed = BeautifulSoup(page,features="html.parser").find("article")
        article = str(parsed).split("\n")
        return article
        
    @staticmethod
    def run():
        index = requests.get("https://www.learncpp.com").text
        text = BeautifulSoup(index,features="html.parser").select(".lessontable-row-title > a")
        page_num = 1
        table_contents_and_links = BookMaker.get_table_of_contents_and_links(text)
        links = table_contents_and_links["links"]

        with open("templates/tableofcontents.html","w",encoding="utf-8") as file:
            file.writelines(table_contents_and_links["text"])

        with concurrent.futures.ProcessPoolExecutor() as executor:
            links = executor.map(BookMaker.get_article,links)
            links = executor.map(BookMaker.get_fixed_lines,links)

        current_link = f"cppbook-pg{page_num}"
        with open(f"templates/{current_link}.html","w",encoding="utf-8") as file:
            file.write(BookMaker.OPENING_TAG)
            file.write(BookMaker.get_header(page_num))
        file = open(f"templates/{current_link}.html","a",encoding="utf-8")
        i = 1

        for article in links:
            section_code= f"<hr><a href={current_link}#lesson{i} name=lesson{i} class=sect>Lesson {i}</a>"
            file.write(section_code)
            i+=1
            file.writelines(article)
            if i % 50 == 0:
                page_num+=1
                current_link= f"cppbook-pg{page_num}"
                template_link= f"templates/{current_link}.html"
                if page_num == 2:
                    file.write(f"""
                        <hr>
                        <div class=footer>
                            <a href={current_link}> <h2>Next Page</h2> </a>
                        </div>
                        """)
                else:
                        prev_link = f"cppbook-pg{page_num - 2}"
                        file.write(f"""
                        <hr>
                        <div class=footer>
                            <a href={prev_link}><h2>Previous Page</h2></a>
                            <a href={current_link}><h2>Next Page</h2></a>
                        </div>
                        """)            
                file.writelines(BookMaker.CLOSING_TAG)
                file.close()
                file = open(template_link,"w",encoding="utf-8")
                file.write(BookMaker.OPENING_TAG)
                file.write(BookMaker.get_header(page_num))
        file.writelines(BookMaker.CLOSING_TAG)
        file.close()   

if __name__ == "__main__":
    BookMaker.run()


