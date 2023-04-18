import requests
import lxml.html as html # para analizar y manipular documentos HTML (para usar Xpath)

import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

# Xpath para obtener los links a los artículos de noticias
XPATH_LINK_TO_ARTICLE = '//text-fill/a[contains(@class, "Sect")]/@href'
# Xpath para obtener el título de un artículo de noticias
XPATH_TITLE = '//h2[not(@class)]/span/text()'
# Xpath para obtener el resumen de un artículo de noticias
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
# Xpath para obtener los nodos 'p' del cuerpo de un artículo de noticias
XPATH_BODY = '//div[@class="html-content"]/p'



def parse_notice(link, today):
    """
    Función que realiza el scraping de un artículo de noticias y guarda la información en un archivo de texto.
    
    Args:
        link (str): Link al artículo de noticias.
        today (str): Fecha actual en formato dd-mm-yy.
    """
    
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            # Obtiene el título, el resumen y el cuerpo del artículo
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                # Quita los saltos de linea al comienzo y final del título
                title = title.strip()
                # Quita los caracteres especiales
                title = ''.join(char for char in title if char.isalnum() or char == ' ')
                # Quita las comillas del título si las tiene
                title = title.replace('\"', '')
                
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                
            except IndexError:
                return
            
            # Guarda la información del artículo en un archivo de texto
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                
                # Extrae el texto de cada nodo 'p' y lo escribe en un archivo de texto
                for p in body:
                    p = p.xpath('.//text()')
                    f.write(''.join(p))
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    """
    Función que realiza el scraping de la página principal de La República y 
    llama a la función parse_notice para cada artículo de noticias encontrado.
    """
    
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parced = html.fromstring(home)
            
            # Obtiene los links a los artículos de noticias de la página principal
            notices_links = parced.xpath(XPATH_LINK_TO_ARTICLE)
            
            # Crea un directorio con la fecha actual si no existe
            today = datetime.date.today().strftime('%d-%m-%y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            # Llama a la función parse_notice para cada artículo de noticias encontrado
            for link in notices_links:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()