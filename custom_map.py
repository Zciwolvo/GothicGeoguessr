from PIL import Image


class CustomMap:
    def __init__(
        self,
        name,
        image_path,
        initial_zoom,
    ):
        self.name = name
        self.image_path = image_path
        params = self.get_image_resolution(self.image_path)
        self.image_width = params[0]
        self.image_height = params[1]
        self.initial_zoom = initial_zoom

    def get_image_resolution(self, image_path):
        with Image.open(image_path) as img:
            width, height = img.size
            return [width, height]

    def to_dict(self):
        return {
            "name": self.name,
            "image_path": self.image_path,
            "initial_zoom": self.initial_zoom,
        }
