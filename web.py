from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

## Implementación de Diccionario 
contenidosubpag = "<p>Contenido general para las subpáginas :D </p>"
contenido = {
    '/': """
    <html>
    </html>
    """,
    '/proyecto/1': f"""
    <html>
        <h1>Ana Lee</h1>
        <h2>Recomendación de libros</h2>

        <p>
        El proyecto consiste en el diseño de un sitio que muestra la informacion
        de distintos libros. La información se obtiene de una base de datos la
        cual se actualiza cada vez que se agrega un nuevo libro. Lorem ipsum dolor
        sit amet, consectetur adipiscing elit. Nulla aliquam faucibus sapien, nec
        eleifend libero pulvinar a. Donec suscipit tortor quis velit placerat, et
        finibus nibh fermentum. Cras eget nunc pretium, aliquet neque sed, porta
        ex. Sed eros nisl, ultricies sit amet nisl ut, euismod euismod ex. Cras
        ipsum enim, porttitor at pharetra non, venenatis iaculis nulla. Praesent
        vel mi non lectus ultricies accumsan eget non lectus. Pellentesque ornare
        lorem et ipsum vestibulum, et eleifend ante sollicitudin. Interdum et
        malesuada fames ac ante ipsum primis in faucibus. Vivamus congue, urna vel
        fermentum lobortis, turpis eros maximus enim, a consectetur quam augue in
        dolor.
        </p>
        <p>
        In non bibendum metus. Phasellus ac laoreet dui, nec viverra enim. Donec
        pharetra ultrices erat nec molestie. Sed interdum dignissim velit in
        consequat. Sed lectus purus, facilisis eu pharetra sit amet, vehicula in
        purus. Cras dictum arcu ante, sed sollicitudin enim interdum ut. Donec
        consectetur, velit a luctus rutrum, orci nunc interdum diam, nec cursus
        risus neque vitae arcu. Mauris est neque, vulputate id est sed, euismod
        sodales felis. Aenean ac ipsum quis lacus fermentum pharetra.
        </p>
    </html>
    """,
    '/proyecto/2': f"""
    <html>
        <h1>¿Qué película o serie me falta ver?</h1>
        {contenidosubpag}
    </html>
    """,
    '/proyecto/3': f"""
    <html>
        <h1>Web para gestión de fotos</h1>
        {contenidosubpag}
    </html>
    """
}

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        ## Agregué una condicional para que el servidor regrese el contenido del archivo en esa ruta
        if self.path == '/': 
             ## Con esta parte abrimos el archivo de home.html como archivo de lectura
            with open('home.html', 'r') as file:
                archivo = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(archivo.encode("utf-8"))
        else:
            ## En caso de que no esté '/' en el path, nos regresaría el error 404 
            response_content = contenido.get(self.path, "<html><h1>404 Not Found</h1></html>")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(response_content.encode("utf-8"))

    def get_response(self):
        ## Para este caso, mandé a pedir el url y dividí el path (que era: proyecto/web-uno?autor=ana)
        ## de manera que me quedara de un lado "proyecto" y del otro "web-uno?autor=ana". 
        ## Luego de ello puse un [-1] para indicar de que lado se iba a tomar la información. 
        proyecto = self.url().path.split('/')[-1]
        
        ## En esta parte mandé a pedir el autor que indicaba en el path. 
        autor = self.query_data().get('autor', '')
        
        ## Modifiqué esta primera línea de h1 con los títulos por defecto "Proyecto" y "Autor",
        ## luego los mandé a llamar {} desde lo que hice en la parte anterior, al extraer la información. 
        return f"""
    <h1> Proyecto: {proyecto} Autor: {autor} </h1>
    <p> URL Parse Result : {self.url()}         </p>
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
"""
        
## En esta parte cambié el puerto 8080 al 8000
if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
