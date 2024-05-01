from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from readabilipy import simple_json_from_html_string
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def capture_web_content(url):
    parsed_url = urlparse(url)
    fragment = parsed_url.fragment
    
    options = FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    
    if fragment:
        try:
            elem = driver.find_element(By.ID, fragment)
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            html_section = driver.execute_script("return arguments[0].outerHTML;", elem)
            # Create a beautifulsoup object from the html
            soup = BeautifulSoup(html_section, 'html.parser')
        except Exception as e:
            print("Couldn't find or load the element with id: ", fragment)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
    else:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

    readable_content = simple_json_from_html_string(str(soup), use_readability=True)

    driver.quit()
    
    text_array = [obj['text'] for obj in readable_content['plain_text']]
    article_content = " ".join(list(dict.fromkeys(text_array)))

    return readable_content["title"], article_content
  