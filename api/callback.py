from http.server import BaseHTTPRequestHandler
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            code = params.get('code', [None])[0]
            
            if not code:
                raise ValueError("Missing auth code")
            
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv("8a19ee685a0245d79e8000662fb28534"),
                client_secret=os.getenv("4aa5f55d5516449289fba4a63cc5b101"),
                redirect_uri=os.getenv("https://mood-miner.vercel.app/api/callback"),
                scope="user-read-recently-played"
            ))
            token = sp.auth_manager.get_access_token(code)
            
            # Redirect back to frontend with token
            self.send_response(302)
            self.send_header('Location', f'/?token={token["access_token"]}')
            self.end_headers()
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())