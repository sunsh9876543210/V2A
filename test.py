from PIL import Image, ImageFilter

image = Image.open('000026.png')
image = image.filter(ImageFilter.FIND_EDGES)
image.save('new_name.png') 