from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

        ## Agregué una condicional para que el servidor regrese el contenido del archivo en esa ruta
        if self.path == '/': 
        ## Con esta parte abrimos el archivo de home.html como archivo de lectura
            with open('home.html', 'r') as file:
                content = file.read()
            self.wfile.write(content.encode("utf-8"))
        ## En caso de que no esté '/' en el path, nos regresaría el error 404
        else:
            self.send_response(404)

    def get_response(self):
        ## Para este caso, mandé a pedir el url y dividí el path (que era: proyecto/web-uno?autor=ana)
        ## de manera que me quedara de un lado "proyecto" y del otro "web-uno?autor=ana". 
        ## Luego de ello puse un [-1] para indicar de que lado se iba a tomar la información. 
        proyecto = self.url().path.split('/')[-1]
        
        ## En esta parte mandé a pedir el autor que indicaba en el path. 
        autor = self.query_data().get('autor', '')
        
        return f"""
        ## Modifiqué esta primera línea de h1 con los títulos por defecto "Proyecto" y "Autor",
        ## luego los mandé a llamar {} desde lo que hice en la parte anterior, al extraer la información. 
    <h1> Proyecto: {proyecto} Autor: {autor} </h1>
    <p> URL Parse Result : {self.url()}         </p>
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
"""


## En esta parte cambié el puerto 8080 al 8000
if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
