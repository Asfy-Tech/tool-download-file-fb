import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from terminal.accounts import Account
from terminal.create_account import create_account
from terminal.create_account import input_account
from terminal.create_account import check_login
from terminal.create_account import switch_account
from terminal.create_account import question_account


def main():
    console = Console()
    console.print(Panel("Chọn một hành động:", style="bold green"))

    choices = [
        "Danh sách tài khoản",
        "Thoát"
    ]
    
    action_question = inquirer.List('action', message="Bạn muốn làm gì", choices=choices, carousel=True)
    
    answers = inquirer.prompt([action_question])

    if answers:
        action = answers['action']
        console.print(f"[bold green]Bạn đã chọn:[/] {action}")
        
        if action == "Danh sách tài khoản":
            question_account()
        else:
            console.print("Thoát chương trình.")
    else:
        console.print("Bạn đã hủy chọn.")
        
if __name__ == "__main__":
    main()