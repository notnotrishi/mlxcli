# Command line interface to run LLMs locally on a Mac using MLX

## Requirements:
- Apple silicon (M series chip) machine with at least 8GB memory
- Python >= 3.8
- macOS >= 13.5

## Setup and Run:
1. Download/clone the repo to your machine
2. Go to the `mlxcli` folder from Terminal and ensure you have the required packages installed:
   `pip3 install --upgrade mlx_lm pynput`
3. Run it using the command:
  `python3 main.py`
4. To generate response after a prompt press `cmd+enter`, or to quit `cmd+q`

## Notes:
- Supports multi-line inputs i.e., you can type multiple lines or paste contents from elsewhere
- The code uses Gemma2-2b-it 4bit (quantized) model by default, but you can change the MLX model in the code to switch (if needed and if your machine can support). See `main.py` for instructions.
- From my experience and LMSYS ratings, Gemma2-2b is a really solid model for edge AI, on consumer-grade hardware. More details: https://developers.googleblog.com/en/smaller-safer-more-transparent-advancing-responsible-ai-with-gemma/
- I have had amazing results with MLX for Gemma2-2b-IT 4 bit -- getting ~40 tokens/sec in generation on a Mac Air M2 8GB, without losing much quality (even with quantization). More details about MLX: https://github.com/ml-explore/mlx
- Experimental, not for prodution use. Feel free to modify it for personal use, but check Gemma's licensing if you modify and distribute further.

## Planned improvements (if/when time permits):
- [ ] Support for streaming responses
- [ ] Options to customize temperature etc. Currently it's hardcoded in code.
- [ ] Check context length/tokens etc. based on model. Gemma2-2b has a context length of 8k.
- [ ] Multi-turn responses. Currently it doesn't take into account previous response i.e., each prompt is new.
- [ ] Test/support structured JSON outputs adhering to a schema