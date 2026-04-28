import requests
import secrets
import hashlib
import base64
import typer
import time
import webbrowser
from urllib.parse import urlparse, parse_qs, urlencode
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from rich.console import Console

from insighta.storage import save_tokens, clear_tokens, load_tokens

app = typer.Typer()
console = Console()

def generate_pkce_pair() -> tuple[str, str]:
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return code_verifier, code_challenge

def start_callback_server(result: dict):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Suppress default HTTP server logging

        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path != "/callback":
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")
                return

            query = parse_qs(parsed.query)
            result["code"] = query.get("code", [None])[0]
            result["state"] = query.get("state", [None])[0]

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Login successful. You can close this window and return to your terminal.")

    server = HTTPServer(("127.0.0.1", 9000), Handler)

    def run():
        server.handle_request() # Processes exactly one request, then shuts down cleanly

    thread = Thread(target=run, daemon=True)
    thread.start()
    time.sleep(0.5)
    return thread

@app.command()
def login():
    with console.status("[cyan]Starting GitHub login...[/cyan]"):
        code_verifier, code_challenge = generate_pkce_pair()
        result = {}
        thread = start_callback_server(result)

        params = urlencode({
            "code_challenge": code_challenge,
            "redirect_uri": "http://localhost:9000/callback"
        })
        auth_url = f"http://127.0.0.1:8000/auth/github?{params}"

    console.print("[bold green]Opening browser for authentication...[/bold green]")
    webbrowser.open(auth_url)

    with console.status("[cyan]Waiting for browser callback...[/cyan]"):
        thread.join(timeout=300) # 5 minutes timeout

    code = result.get("code")
    state = result.get("state")

    if not code:
        console.print("[bold red]Login failed: No authorization code received.[/bold red]")
        return

    with console.status("[cyan]Exchanging token with backend...[/cyan]"):
        res = requests.post(
            "http://127.0.0.1:8000/auth/github/token",
            json={
                "code": code,
                "code_verifier": code_verifier,
                "state": state,
                "redirect_uri": "http://localhost:9000/callback"
            }
        )

    if res.status_code != 200:
        console.print(f"[bold red]Login failed: {res.json()}[/bold red]")
        return

    data = res.json()
    save_tokens(data)
    console.print(f"[bold green]✔ Logged in as @{data['user']['username']}[/bold green]")

@app.command()
def logout():
    data = load_tokens()
    if data and "refresh_token" in data:
        with console.status("[cyan]Invalidating session securely...[/cyan]"):
            try:
                requests.post(
                    "http://127.0.0.1:8000/auth/logout", 
                    json={"refresh_token": data["refresh_token"]}
                )
            except Exception:
                pass # Fail silently if backend is unreachable; local wipe is priority

    clear_tokens()
    console.print("[bold green]✔ Logged out successfully.[/bold green]")

@app.command()
def whoami():
    data = load_tokens()
    if not data or "user" not in data:
        console.print("[bold yellow]Not logged in. Run `insighta login`.[/bold yellow]")
        return
    console.print(f"[bold green]Logged in as @{data['user']['username']} ({data['user']['role']})[/bold green]")