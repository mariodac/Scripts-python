from rembg import remove
from PIL import Image
from pathlib import Path
from os import environ
root_path = Path(environ['USERPROFILE']) / 'Downloads'
input_path = 'input.png'
output_path = 'output.png'
inp = Image.open(root_path / input_path)
output = remove(inp)
output.save(root_path / output_path)
Image.open(root_path / output_path)