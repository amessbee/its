from PIL import Image

def invert_image_colors(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Invert the image colors
    inverted_image = Image.eval(image, lambda x: 255 - x)

    # Save the inverted image back to the same file
    inverted_image.save(image_path)

# Provide the path to your JPG file
jpg_file_path = '../logo.jpg'

# Call the function to invert the colors and save the image
invert_image_colors(jpg_file_path)
