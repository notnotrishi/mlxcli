## sample code to quantize a model using MLX
# from mlx_lm import convert

# # help(convert)
# repo = "mlx-community/gemma-2-2b-it"
# convert(repo, quantize=True, q_bits=4)
# print('done')

## sample code to run it from local folder
# from mlx_lm import load, generate

# model, tokenizer = load('mlx_model')
# response = generate(model, tokenizer, prompt="what is life?", verbose=True)
# print(response)