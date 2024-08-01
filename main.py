from mlx_lm import load, generate
import sys
import time
import threading
import textwrap
from pynput import keyboard

# ANSI color codes for command line
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[38;5;108m"

def format_prompt(user_input):
    return f"<bos><start_of_turn>user\n{user_input}<end_of_turn>\n<start_of_turn>model"

def colored_print(text, color):
    sys.stdout.write(color + text + RESET)
    sys.stdout.flush()

def styled_print(text, style):
    sys.stdout.write(style + text + RESET)
    sys.stdout.flush()

class Spinner:
    def __init__(self, message=""):
        self.message = message
        self.spinning = False
        self.spinner_chars = "|/-\\"

    def spin(self):
        i = 0
        while self.spinning:
            sys.stdout.write(f"\r{self.message} {self.spinner_chars[i]} ")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(self.spinner_chars)

    def __enter__(self):
        self.spinning = True
        threading.Thread(target=self.spin, daemon=True).start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spinning = False
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

def get_multiline_input():
    # print("Type/paste your prompt and press cmd+enter to generate, or cmd+q to exit:")
    lines = []
    is_done = False

    cmd_pressed = False
    enter_pressed = False

    def on_press(key):
        nonlocal is_done, cmd_pressed, enter_pressed
        if key == keyboard.Key.cmd:
            cmd_pressed = True
        
        if key == keyboard.Key.enter:
            enter_pressed = True

        if cmd_pressed and enter_pressed:
            is_done = True
            return False

    def on_release(key):
        nonlocal cmd_pressed, enter_pressed
        if key == keyboard.Key.cmd:
            cmd_pressed = False
                
        if key == keyboard.Key.enter:
            enter_pressed = False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while not is_done:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break

    listener.stop()

    return '\n'.join(lines)

def main():
    print("Loading model. This may take a few moments...")
    # defaults to gemma2-2b-it int4. change the model below if your Mac can support higher precision or if you'd prefer other models
    # other options found at https://huggingface.co/mlx-community
    model, tokenizer = load("mlx-community/gemma-2-2b-it-4bit")
    print("Model loaded. You can now start interacting with AI.")

    while True:
        styled_print("\nType/paste your prompt and press cmd+enter to generate, or cmd+q to exit:\n", BOLD)
        user_input = get_multiline_input()            
        
        # removes any common leading whitespace from every line
        user_input = textwrap.dedent(user_input)
        
        formatted_prompt = format_prompt(user_input)
        
        # start the spinner
        with Spinner("Generating response..."):
            response = generate(model, tokenizer, prompt=formatted_prompt, verbose=False, max_tokens=1000, temp=0.3)
        
        # extract the model's response from between the tags
        model_response = response.split("<start_of_turn>model\n")[-1].split("<end_of_turn>")[0].strip()
        
        colored_print(f"\n{model_response}\n", GREEN)

if __name__ == "__main__":
    main()