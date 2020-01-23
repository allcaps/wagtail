import os

from django.conf import settings
from PIL import Image, ImageDraw


def dashed_line(draw, x1, y1, x2, y2, line=9, gap=9, color="#ff00ea", stroke_width=4):
    if x1 == x2:  # Vertical line
        x = x1
        for y in range(y1, y2, line + gap):
            draw.line([x, y, x, min(y + line, y2)], fill=color, width=stroke_width)

    if y1 == y2:  # Horizontal line
        y = y1
        for x in range(x1, x2, line + gap):
            draw.line([x, y, min(x + line, x2), y], fill=color, width=stroke_width)


def rectangle(draw, x, y, width, height):
    # Adjust the box so it is on the outside of the element.
    x -= 4
    y -= 4
    width += 4 + 1
    height += 4 + 1
    dashed_line(draw, x, y, x + width, y)  # top
    dashed_line(draw, x + width, y, x + width, y + height)  # right
    dashed_line(draw, x, y + height, x + width, y + height)  # bottom
    dashed_line(draw, x, y, x, y + height)  # left


class DocumentationFactory:
    def __init__(self, filename, title, driver):
        self.blocks = []
        self.filename = os.path.join(settings.BASE_DIR, "..", "editor_manual", filename)
        self.h1(title)
        self.driver = driver

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        with open(self.filename, "w") as doc:
            doc.write("\n\n".join(self.blocks))

    def h1(self, content):
        self.blocks.append(f"{content}\n" f"{len(content) * '='}")

    def h2(self, content):
        self.blocks.append(f"{content}\n{len(content) * '-'}")

    def p(self, content):
        self.blocks.append(content)

    def img(self, filename, element=None):
        full_file_path = os.path.join(settings.BASE_DIR, "..", "_static", "images", filename)
        self.driver.save_screenshot(full_file_path)
        self.blocks.append(f".. image:: /_static/images/{filename}")
        if element:
            im = Image.open(full_file_path)
            draw = ImageDraw.Draw(im)
            pos_x = element.location["x"]

            # Compensate y position for the window y offset.
            offset_y = int(self.driver.execute_script("return window.pageYOffset;"))
            pos_y = element.location["y"] - offset_y

            width = element.size["width"]
            height = element.size["height"]
            rectangle(draw, pos_x, pos_y, width, height)
            im.save(full_file_path, format="PNG")
