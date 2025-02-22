from enum import Enum

class GrayScale(Enum):
    """
    Represent Gray Scale level for ASCII art.
    These values are stored as strings, with a range of characters that progress from darkest to lightest.
    """

    LEVEL_70 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    LEVEL_10 = "@%#*+=-:. "

if __name__ == "__main__":
    pass
