from rembg import remove
from PIL import Image
from pathlib import Path
root_path = Path(__file__).parent
input_path = 'teste.jpg'
output_path = 'multiversus.png'
inp = Image.open(root_path / input_path)
output = remove(inp)
output.save(root_path / output_path)
Image.open(root_path / output_path)