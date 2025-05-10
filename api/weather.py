from http.server import BaseHTTPRequestHandler
import requests
import os
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = dict(qc.split('=') for qc in query.split('&')) if query else {}
            city = params.get('city', '')
            
            if not city:
                raise ValueError("City parameter missing")
                
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    'q': city,
                    'appid': os.getenv("07d2b2e3489bbf7f1b0c60083089d13d"),
                    'units': 'metric'
                }
            )
            response.raise_for_status()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))