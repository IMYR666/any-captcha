# coding: utf-8
import base64
import os
import random
from io import BytesIO

from PIL import Image
from PIL.ImageDraw import Draw


class CaptchaUtils(object):
    @staticmethod
    def random_choice_from(_range):
        return random.choice(_range)

    @staticmethod
    def random_color_bg():
        bg = [0xF0D8F0, 0xF0D8FF, 0xC0F0D8, 0xF0F0C0, 0xD8F0C0, 0xD8C0F0, 0xD8C0D8, 0xC0D8C0, 0xF0D8D8,
              0xF0C0C0, 0xC0C0F0, 0xD8D8FF]
        return CaptchaUtils.get_rgb(CaptchaUtils.random_choice_from(bg), 160)

    @staticmethod
    def random_color_fg():
        bg = [0x301878, 0x184830, 0x606030, 0x603018, 0x601878, 0x303078, 0x303030, 0x186018, 0x303090, 0x304860,
              0x306048, 0x304848, 0x481860, 0x181818, 0x186030, 0x606048, 0x181848, 0x487818, 0x607830]
        return CaptchaUtils.get_rgb(CaptchaUtils.random_choice_from(bg))

    @staticmethod
    def draw_line(image, start_p, end_p, color, wdith=2):
        points = [start_p[0], start_p[1], end_p[0], end_p[1]]
        Draw(image).line(points, fill=color, width=wdith)

    @staticmethod
    def draw_rectangle(image, box, color):
        points = [(box[0], box[1]), (box[0] + box[2], box[1]), (box[0] + box[2], box[1] + box[3]),
                  (box[0], box[1] + box[3]), (box[0], box[1])]

        for index in range(len(points) - 1):
            CaptchaUtils.draw_line(image, points[index], points[index + 1], color)

    @staticmethod
    def draw_dot(image, color, width=2):
        w, h = image.size
        draw = Draw(image)
        x1 = random.randint(0, w)
        y1 = random.randint(0, h)
        draw.line((x1, y1, x1 - 1, y1 - 1), fill=color, width=width)

    @staticmethod
    def get_rgb(color_hex, op=None):
        if isinstance(color_hex, str):
            color_hex = int(color_hex, 16)

        if op is None:
            return (color_hex & 0xff0000) >> 16, (color_hex & 0x00ff00) >> 8, (color_hex & 0x0000ff)
        else:
            return (
                (color_hex & 0xff0000) >> 16, (color_hex & 0x00ff00) >> 8, (color_hex & 0x0000ff),
                random.randint(op, 200))

    @staticmethod
    def random_point(w, h):
        return random.randint(0, w), random.randint(0, h)

    @staticmethod
    def transform_base64_to_image(base64_str, image_path, image_name):
        if not os.path.isdir(image_path):
            os.makedirs(image_path)

        with open(os.path.join(image_path, image_name), "wb") as fh:
            fh.write(base64.decodebytes(bytes(base64_str, "utf-8")))

    @staticmethod
    def convert_gif_to_jpg(gif_file, jpg_file_path):
        try:
            im = Image.open(gif_file)
        except IOError:
            print("converting failed while converting gif to jpg.")
            return -1

        i = 0
        mypalette = im.getpalette()
        # print(gif_file)
        try:
            while 1:
                im.putpalette(mypalette)
                new_im = Image.new("RGB", im.size)
                new_im.paste(im)
                new_im.save(jpg_file_path)

                i += 1
                im.seek(im.tell() + 1)

        except EOFError:
            pass  # end of sequence

    @staticmethod
    def convert_gif_2_jpg(gif_base64):
        bas = base64.decodebytes(bytes(gif_base64, "utf-8"))
        im = Image.open(BytesIO(bas))
        i = 0
        mypalette = im.getpalette()
        base64_jpgs = []
        try:
            while 1:
                im.putpalette(mypalette)
                new_im = Image.new("RGB", im.size)
                new_im.paste(im)
                buffered = BytesIO()
                new_im.save(buffered, format="JPEG")
                img_data_base64 = base64.b64encode(buffered.getvalue())
                base64_jpgs.append(img_data_base64)
                i += 1
                im.seek(im.tell() + 1)

        except EOFError:
            pass

        return base64_jpgs
