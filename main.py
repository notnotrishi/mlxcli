from mlx_lm import load, generate
import sys
import time
import threading

# ANSI color codes
# YELLOW = "\033[93m"
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
            time.sleep(0.01)
            i = (i + 1) % len(self.spinner_chars)

    def __enter__(self):
        self.spinning = True
        threading.Thread(target=self.spin, daemon=True).start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spinning = False
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

def main():
    print("Loading model. This may take few moments...")
    model, tokenizer = load("mlx-community/gemma-2-2b-it-4bit")
    print("Model loaded. You can now start interacting with the Gemma.")

    while True:
        styled_print("\nEnter your prompt (or 'q' to quit): ", BOLD)
        user_input = input()
        
        if user_input.lower() == 'q':
            print("Exiting the program. Goodbye!")
            break
        
        formatted_prompt = format_prompt(user_input)
        
        # start the spinner
        with Spinner("Generating response..."):
            response = generate(model, tokenizer, prompt=formatted_prompt, verbose=False, max_tokens=1000, temp=0.3)
        
        # extract the model's response from between the tags
        model_response = response.split("<start_of_turn>model\n")[-1].split("<end_of_turn>")[0].strip()
        
        colored_print(f"\n{model_response}\n", GREEN)

if __name__ == "__main__":
    main()