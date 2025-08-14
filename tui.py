import requests
from rich.console import Console
from rich.panel import Panel

console = Console()

def test_connection():
    try:
        response = requests.get('http://localhost:5000/health')
        print(response.json())
    except Exception as e:
        print(f"Error:{e}")

test_connection()
