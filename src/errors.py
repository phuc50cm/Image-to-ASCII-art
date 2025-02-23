class ImageNotFound(Exception):
    def __init__(self, img_filepath, msg="Image not found"):
        super().__init__(f"{msg}: {img_filepath}")


class ImageTooSmall(Exception):
    def __init__(self, msg="Image too small to convert"):
        super().__init__(f"{msg}")

