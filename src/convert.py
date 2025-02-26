import argparse

from ascii_converter import AsciiConverter
from grayscale import GrayScale

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="the file being converted")
    parser.add_argument("-c", "--cols", type=int,
                        help="the resolution of result image")
    parser.add_argument("-l", "--level", type=int, choices=[10, 70], default=70,
                        help="gray scale level")
    args = parser.parse_args()

    if args.level == 70:
        ascii_converter = AsciiConverter(GrayScale.LEVEL_70)
    else:
        ascii_converter = AsciiConverter(GrayScale.LEVEL_10)
    
    ascii_converter.img_to_ascii(args.file, args.cols)

if __name__ == "__main__":
    main()
