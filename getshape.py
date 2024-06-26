import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image

def generate_char_image(char, font, img_size=(32, 32)):
    """
    Generate an image array for a given character.
    """
    # Create a blank image with white background
    img = Image.new('L', img_size, color=255)
    draw = ImageDraw.Draw(img)
    
    # Get the size of the character
    text_size = font.getbbox(char)
    
    # Calculate position to center the character
    text_x = (img_size[0] - text_size[0]) // 2
    text_y = (img_size[1] - text_size[1]) // 2
    
    # Draw the character onto the image
    draw.text((text_x, text_y), char, font=font, fill=0)
    
    # Convert image to numpy array
    img_array = np.array(img)
    return img_array

def find_most_similar_char(image_array, charset, font_path='arial.ttf', font_size=32, img_size=(32, 32)):
    """
    Find the character in the charset that is most similar to the given image array.
    """
    # Load the font once
    font = ImageFont.truetype(font_path, font_size)
    
    min_diff = float('inf')
    best_char = None
    
    for char in charset:
        char_img = generate_char_image(char, font, img_size)
        
        # Calculate the difference between the images using vectorized operations
        diff = np.sum((image_array - char_img) ** 2)
        
        if diff < min_diff:
            min_diff = diff
            best_char = char
            
    return best_char

def convert(image_array, cols, scale, i):
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`~!@#$%^&*()-=_+[]{};\':\"\\/?,.<>█ |"
    image = np.transpose(image_array)

    W, H = image.shape[0], image.shape[1]
    w = W / cols
    h = w / scale
    rows = int(H / h)

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
    
    aimg = []

    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        if j == rows - 1:
            y2 = H

        aimg.append("")

        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            if i == cols - 1:
                x2 = W
            
            img = image[x1 : x2, y1 : y2]
            gsval = find_most_similar_char(img.transpose(), charset = charset, font_size = x2-x1, img_size = (x2-x1, y2-y1) )
            #print(gsval)
            aimg[j] += gsval
    
    return aimg, cols, rows
# Example usage
if __name__ == "__main__":
    # Example charset and numpy image array
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`~!@#$%^&*()-=_+[]{};\':\"\\/?,.<>█"
    example_image_array = generate_char_image('')  # Replace this with your actual numpy image array
    most_similar_char = find_most_similar_char(example_image_array, charset)
    print(f"The most similar character is: {most_similar_char}")