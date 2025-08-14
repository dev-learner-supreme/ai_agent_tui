import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

def display_welcome():
    title = Text("AI Agent Terminal Chat", style="bold cyan")
    console.print(Panel(title, title="Welcome", border_style="green"))
    console.print("Type 'quit' to exit, or 'clear' to clear the screen\n", style="dim")

def send_chat_message(message):
    try:
        response = requests.post('http://localhost:5000/chat', json={'message':message}, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}:{response.text}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to AI server is it running?"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out AI is taking too long to respond."}
    except Exception as e:
        return {"error":f"Unexpected error: {str(e)}" }


def main():
    display_welcome()

    while True:
        user_input = Prompt.ask("[bold green]You[/bold green]")

        if user_input.lower() == "quit":
            console.print("\nGoodbye thanks for chatting!", style="bold blue")
            break
        elif user_input.lower() == "clear":
            console.clear()
            display_welcome()
            continue

        if not user_input.strip():
            console.print("Please enter a message", style="yellow")
            continue

        with console.status("[dim]AI is thinking...[/dim]"):
            result = send_chat_message(user_input)

        if 'error' in result:
            console.print(f"\nError: {result['error']}", style="bold red")
        else:
            ai_response = result['ai_response']
            console.print(Panel(ai_response, title="AI response", border_style="blue"))

        console.print()

if __name__ == "__main__":
    main()
