# scraper-de-noticias
Este repositorio contiene un script de Python que realiza web scraping en el sitio web de La República Colombia para extraer noticias y guardarlas en archivos de texto plano.

## Configuración del entorno de trabajo y buenas prácticas 
- Crear una carpeta para el proyecto.
- Iniciar un repositorio de Git.
- Crear un entorno virtual.
- Crear el archivo .gitignore
- Instalar las librerías, en este caso:
	```bash
	pip install -r requirements.txt
	```
	1.  Request: Para realizar peticiones.
	2.  Lxml: Para manipular el documento html y utilizar Xpath
	
- Actualizar pip si este lo sugiere también es una buena práctica:
```bash
	python.exe -m pip install --upgrade pip
```

## Construcción de las expresiones de XPath
### Extraer los links de las noticias:
```
'//h2/a[contains(@class, "Sect")]/@href'
```
>[!note] Nota 
>Por alguna razón que la librería `requests` cambia los nodos `h2` por `text-fill`. Solamente pasa a la hora de obtener los links.
>Por eso en el código se coloca `text-fill` en lugar de `h2`.

En el navegador:
```
$x('//h2/a[contains(@class, "Sect")]/@href').map(x => x.value)
```

### Extraer el título de la noticia:
```
'//h2[not(@class)]/span/text()'
```
En el navegador:
```
$x('//h2[not(@class)]/span/text()').map(x => x.wholeText)
```

### Extraer el resumen de la noticia:
```
'//div[@class="lead"]/p/text()'
```
En el navegador:
```
$x('//div[@class="lead"]/p/text()').map(x => x.wholeText)
```

### Extraer el cuerpo de la noticia
Con este Xpath se obtienen los nodos 'p' dentro del body.
```
'//div[@class="html-content"]/p'
```

## Funciones
### parse_notice(link, today)
Función que realiza el scraping de un artículo de noticias y guarda la información en un archivo de texto.
    
   Args:
        - link (str): Link al artículo de noticias.
        - today (str): Fecha actual en formato dd-mm-yy.
        
### parse_home()
Función que realiza el scraping de la página principal de La República y llama a la función parse_notice para cada artículo de noticias encontrado.
