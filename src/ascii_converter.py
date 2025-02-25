import os
from PIL import Image, ImageDraw, ImageFont
from grayscale import GrayScale
import numpy as np
from errors import ImageTooSmall

class AsciiConverter:
    def __init__(self, grayscale_level=GrayScale.LEVEL_70):
        self.grayscale_level = grayscale_level
        self.ascii = self.grayscale_level.value
        self.level = len(self.ascii) - 1
        self.font_path = "../fonts/FiraMono-Regular.ttf"
        self.font_size = 1


    def img_to_ascii(self, img_filepath, cols, font_scale):
        # Open image and convert to grayscale
        image = Image.open(img_filepath).convert('L')

        # Get size of row and col of tiles
        image_width, image_height = image.width, image.height
        tile_width = image_width / cols
        tile_height = tile_width / font_scale
        rows = int(image_height / tile_height)

        """
        print(image_width, image_height)
        print(tile_width, tile_height)
        print(cols, rows)
        """

        # Check if image is to small to represenet
        if cols > image_width or rows > image_height:
            raise ImageTooSmall()

        # Create list of character string to store ascii
        ascii_art = []
        # Generate list of dimensions 
        for j in range(rows):
            y1 = int(j * tile_height)
            y2 = int((j + 1) * tile_height)

            # Correct the last tile to the end of image height
            if j == rows - 1:
                y2 = image_height

            # Append the characters row
            ascii_art.append("")

            for i in range(cols):
                x1 = int(i * tile_width)
                x2 = int((i + 1) * tile_width)

                # Correct the lsat tile to the end of image width
                if i == cols - 1:
                    x2 = image_width

                # Crop the image to tile
                tile_image = image.crop((x1, y1, x2, y2)) 
                avg_tile_luminace = avg_luminance(tile_image)

                # Look up ascii char
                ascii_char = self._get_ascii_char(avg_tile_luminace)
                ascii_art[j] += ascii_char
                
                # Write to file
                #self._ascii_to_file(ascii_art, img_filepath)

        self._ascii_to_image(ascii_art, cols, rows, image_width, image_height)

        image.close()

    def _get_ascii_char(self, avg_value):
        """
        Calute gray scale char base on the average luminance.

        Args: average luminane value.
        Return ascii char based on grayscale
        """
        char = self.ascii[int((avg_value * self.level) / 255)]
        return char

    def _ascii_to_file(self, ascii_art, img_filepath):
        """
        Take an array of ascii_char and write it to text file.

        Args: acsii_art is an acsii array of string and image file path
        Output a text file with same name as image file path
        """
         
        base_file_name = os.path.basename(img_filepath)
        output_file = f"{os.path.splitext(base_file_name)[0]}.txt"

        file = open(output_file, 'w')
        for row in ascii_art:
            file.write(row + '\n')
        file.close()
    
    def _ascii_to_image(self, ascii_art, cols, rows, original_width, original_height):
        """
        Take an array of ascii char and create image of it

        Args: ascii_art is an acsii array of string and
        Create a image file
        """
        #image = Image.new("RGB", (image_width, image_height), "white")
        #draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(self.font_path, 10)

        # Start creating image
        bbox = font.getbbox("A")
        char_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]

        image_width = cols * char_width
        image_height = rows * line_height
        image = Image.new("RGB", (image_width, image_height), "white")
        draw = ImageDraw.Draw(image)
            
        x, y = 0, 0
        for line in ascii_art:
            draw.text((x, y), line, font=font, fill="black")
            y += line_height

        image = image.resize((original_width, original_height), resample=Image.Resampling.LANCZOS)
        image.save("test.png")

    def set_new_font(self, new_font_path):
        self.font_path = new_font_path

    def _find_best_font_size(self, draw, text, max_width):
        self.font_size = 1
        while True:
            font = ImageFont.truetype(self.font_path, self.font_size)
            text_width = draw.textlength(text, font=font)
            if text_width > max_width:
                self.font_size -= 1
                return 
            self.font_size += 1

def avg_luminance(image):
    """
    Calculate average luminance of a tile (w * h size).

    Args: image is PIL Image Object.
    Return avg luminance of an image.
    """
    image_array = np.array(image)
    tile_width, tile_height = image_array.shape
    return np.average(image_array.reshape(tile_width * tile_height))
