import os
import openai
import colorama
from colorama import Fore, Style

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_MESSAGE = "You are AskGPT, a command line tool which can tell user " \
        "the right command to use in the linux command line."

DEFAULT_PROMPT = "Please help me find the linux comamnd which can:\n"

def request_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response

def add_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    return box

def insert_newlines(string, every=64):
    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i:i+every])
    return '\n'.join(lines)

def print_gpt_message(msg):
    print(Fore.GREEN + "AskGPT:")
    msg = insert_newlines(msg)
    boxed_msg = add_msg_box(msg)
    print(Fore.GREEN + boxed_msg)
    print(Style.RESET_ALL)


def main():
    print("Hi! I am AskGPT, a command line tool which can help you "\
            "based on the OpenAI's ChatGPT model. Any question for me?\n")

    messages = [
          {"role": "system", "content": SYSTEM_MESSAGE},
    ]
    while True:
        print("You:")
        user_input = input()
        msg = {"role": "user", "content": DEFAULT_PROMPT + user_input}
        messages.append(msg)
        res = request_gpt(messages)
        ret_msg = res["choices"][0]["message"]
        content = ret_msg["content"]
        print("")
        print_gpt_message(content)
        messages.append(ret_msg)


if __name__ == "__main__":
    main()
