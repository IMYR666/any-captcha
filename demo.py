# coding: utf-8

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


def main():
    project_name = "demo"
    with open("configs/%s.json" % project_name, encoding="utf-8") as fp:
        demo_config = json.load(fp)

    demo_factory = CaptchaFactory(char_custom_fns=[char_custom_fn], bg_custom_fns=[bg_custom_fn], **demo_config)
    index = 3
    while index:
        captcha = demo_factory.generate_captcha()
        captcha.save("output/%s/%s.jpg" % (project_name, captcha.text))
        print(captcha.text, captcha.num)

        index -= 1


if __name__ == "__main__":
    main()
