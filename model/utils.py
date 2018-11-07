# coding: utf-8
import base64
import os
import random
import re
from io import BytesIO

import requests

import numpy as np
import cv2
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


if __name__ == "__main__":
    nums = 0
    files = os.listdir("../output/tmp/")
    gif_base64 = "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"
    base64_jpgs = CaptchaUtils.convert_gif_2_jpg(gif_base64)
    print(base64_jpgs)
    # for file in files:
    #     CaptchaUtils.convert_gif_to_jpg("../output/tmp/%s" % file,
    #                                     "../output/tmp11/%s" % file)
    # for i in range(488560, 488649):
    #     print(i)
    #     url = 'http://www.58guakao.com/user/%d.html' % i
    #     response = requests.get(url)
    #     content = response.content.decode("utf-8")
    #     res = re.findall("\"data:image/gif;base64,(.+?)\"", content)
    #     for re1 in res:
    #         CaptchaUtils.transform_base64_to_image(re1, "../output/actual_captcha_58/", "%s.gif" % nums)
    #         # CaptchaUtils.convert_gif_to_jpg("../output/actual_captcha_58/%s.gif" % nums,
    #         #                                 "../output/actual_captcha_58/%s.jpg" % nums)
    #         nums += 1
