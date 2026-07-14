from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import multiprocessing

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Jarvis is online!']

def start_bot():
    from jarvis_bot import main
    main()

# Start bot immediately (not inside if __name__)
bot_process = multiprocessing.Process(target=start_bot, daemon=True)
bot_process.start()