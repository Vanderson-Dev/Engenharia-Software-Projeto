from http.server import HTTPServer, SimpleHTTPRequestHandler

host = "localhost"
port = 8000

print(f"Servidor rodando em http://{host}:{port}")
print("Pressione CTRL+C para parar")

server = HTTPServer((host, port), SimpleHTTPRequestHandler)
server.serve_forever()
