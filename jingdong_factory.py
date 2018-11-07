# coding: utf-8
import json
import sys

sys.path.append("..")
from PIL import Image
from PIL import ImageFilter

from model.capthafactory import CaptchaFactory
from model.utils import CaptchaUtils


def custom_fn(single_char):
    # do something you wanted
    # return single_char.filter(ImageFilter.GaussianBlur)
    return single_char


def bg_custom_fn(bg):
    # do something you wanted
    # return bg.filter(ImageFilter.GaussianBlur)
    CaptchaUtils.draw_line(bg, (0, CaptchaUtils.random_choice_from(range(12, 14))),
                           (85, CaptchaUtils.random_choice_from(range(13, 15))),
                           CaptchaUtils.get_rgb("0x595e12"), 1)
    CaptchaUtils.draw_line(bg, (0, CaptchaUtils.random_choice_from(range(11, 16))),
                           (85, CaptchaUtils.random_choice_from(range(17, 21))), CaptchaUtils.get_rgb("0x563c7c"), 1)
    return bg


if __name__ == "__main__":
    project_name = "jingdong"
    with open("configs/%s.json" % project_name, encoding="utf-8") as fp:
        demo_config = json.load(fp)

    demo_factory = CaptchaFactory(char_custom_fns=[custom_fn], bg_custom_fns=[bg_custom_fn], **demo_config)
    number = 3
    while number:
        # captcha = demo_factory.generate_captcha(specific_chars=specific)
        captcha = demo_factory.generate_captcha()
        captcha.save("output/%s/" % project_name + captcha.text + ".jpg")
        # for c in captcha.chars:
        #     print(c.char_text, c.color)
        print(captcha.text, captcha.num)

        number -= 1
