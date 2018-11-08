# coding: utf-8

"""
target captcha url: http://www.58guakao.com/user/487549.html
"""
import json
import random

from PIL import Image
from PIL import ImageFilter

from model.capthafactory import CaptchaFactory
from model.utils import CaptchaUtils


def char_custom_fn(single_char):
    # do something you wanted
    # return single_char.filter(ImageFilter.GaussianBlur)
    return single_char


def bg_custom_fn(bg):
    # do something you wanted
    # return bg.filter(ImageFilter.GaussianBlur)
    return bg


def generate_phone_number(idx=0):
    sec = [3, 5, 8]
    other = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    s1, s2 = False, False
    if idx % 2 == 0:
        s1 = True
    if idx % 4 == 0:
        s2 = True

    res = "1"
    for i in range(2, 12):
        if i == 2:
            res += str(random.choice(sec))
        elif i == 3:
            res += str(random.choice(other)) + "-" if s1 else str(random.choice(other))
        elif i == 7 and s2:
            res += str(random.choice(other)) + "-" if s2 else str(random.choice(other))
        else:
            res += str(random.choice(other))

    return res


def generate_mobile_number(idx=0):
    def generate_area_code(idx=0):
        lens = 3 + idx % 2
        return "0" + "".join([str(random.choice(range(0, 10))) for i in range(1, lens)])

    res = ""
    if idx % 3 == 0:
        res += generate_area_code(idx) + "-"
    for i in range(8):
        res += str(random.choice(range(0, 10)))

    return res


def main():
    project_name = "58gua_kao"
    with open("configs/%s.json" % project_name, encoding="utf-8") as fp:
        demo_config = json.load(fp)

    demo_factory = CaptchaFactory(char_custom_fns=[char_custom_fn], bg_custom_fns=[bg_custom_fn], **demo_config)
    index = 3
    while index:
        # text = generate_phone_number(index)
        text = generate_mobile_number(index)

        captcha = demo_factory.generate_captcha(text=text)
        captcha.save("output/%s/%s.jpg" % (project_name, captcha.text))
        print(captcha.text, captcha.num)

        index -= 1


if __name__ == "__main__":
    main()
