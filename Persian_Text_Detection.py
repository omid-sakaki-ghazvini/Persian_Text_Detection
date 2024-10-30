import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont, Image, ImageDraw
import easyocr
import matplotlib.pyplot as plt
import cv2


fontFile = "Sahel.ttf"
imageFile = "example.jpg"

# load the font and image
font = ImageFont.truetype(fontFile, 18)
image = Image.open(imageFile)

# instance text detector
reader = easyocr.Reader(['fa'] ,gpu=False)

# detect text on image
text_ = reader.readtext(imageFile)

threshold = 0.25
# draw bbox and text
for t_, t in enumerate(text_):
    bbox, text, score = t
    reshaped_text = arabic_reshaper.reshape(text)  # correct its shape
    text = get_display(reshaped_text)              # correct its direction
    print(text)

    draw = ImageDraw.Draw(image)
    
    if score > threshold:

        draw.rectangle([(int(bbox[0][0])-5, int(bbox[0][1])-5), (int(bbox[2][0])+5, int(bbox[2][1])+5)], outline ="green", width=4)
        draw.text([int(bbox[0][0])-30, int(bbox[0][1])-30], text, (0,128,0), align='center', font=font)
        draw = ImageDraw.Draw(image)


# save it
image.save("output.jpg")

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 4))

inp_img = cv2.imread("example.jpg")
inp_img = cv2.cvtColor(inp_img, cv2.COLOR_BGR2RGB)

out_img = cv2.imread("output.jpg")
out_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB)

axs[0].imshow(inp_img)
axs[0].set_title('Input Image')

axs[1].imshow(out_img)
axs[1].set_title('Output Image')

# Display the subplots
plt.tight_layout()
plt.show()