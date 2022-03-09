from PIL import Image
import base64
from io import BytesIO
from flask import Flask
import numpy as np

app = Flask(__name__)

@app.route("/")
def stickman():

    img1 = Image.open("layers/image0.png")
    
    img2 = Image.open("layers/image5.png")
    
    # Pasting
    img1.paste(img2, (0,0), mask = img2)

    img1 = img1.convert('RGBA')

    data = np.array(img1)
    red, green, blue, alpha = data.T
    black_areas = (red == 0) & (blue == 255) & (green == 0)
    data[..., :-1][black_areas.T] = (0, 0, 255) # Transpose back needed
    
    img_final = Image.fromarray(data)

    #img_final.show()

    buffered = BytesIO()
    img_final.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    #print(img_str)
    return img_str

app.run(host='0.0.0.0', port=8181)
  
