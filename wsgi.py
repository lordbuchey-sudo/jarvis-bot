from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys
import subprocess

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Jarvis is online!']

# Start the bot as a separate process
import multiprocessing
def start_bot():
    from jarvis_bot import main
    main()

if __name__ == "__main__":
    # Start bot in a separate process
    bot_process = multiprocessing.Process(target=start_bot, daemon=True)
    bot_process.start()