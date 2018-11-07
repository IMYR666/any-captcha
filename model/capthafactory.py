# coding: utf-8
import os

from model.utils import CaptchaUtils

from model.captcha import Captcha


class CaptchaFactory(object):
    def __init__(self, char_custom_fns=None, bg_custom_fns=None, **kwargs):
        self._kwargs = kwargs
        self._char_custom_fns = char_custom_fns
        self._bg_custom_fns = bg_custom_fns
        self._num = self._kwargs.get("num", 4)
        self._texts = self._kwargs.get("texts", ["yangrui"])
        self._bgs = self._kwargs.get("bgs", ["0xffffff"])

        self.init()

    def init(self):
        self.init_text()
        self.init_background()

    def init_text(self):
        if len(self._texts) == 1:
            unknown_string = self._texts[0]
            if os.path.isfile(unknown_string):
                with open(unknown_string, encoding="utf-8") as fp:
                    self._texts = fp.readlines()

    def init_background(self):
        # 如果长度为1，须判断是文件，路径还是颜色字符串
        if len(self._bgs) == 1:
            unknown_string = self._bgs[0]
            if os.path.isfile(unknown_string):  # unknown_string.lower().endswith(".csv")
                # 如果是文件，则默认文件中的内容为颜色字符串，一行一个
                with open(unknown_string) as fp:
                    self._bgs = fp.readlines()
            elif os.path.isdir(unknown_string):
                # 如果是路径，则默认路径中的每个文件都是一张图片
                files = os.listdir(unknown_string)
                self._bgs = [os.path.join(unknown_string, file) for file in files if
                             file.lower().endswith(".jpg") or file.lower().endswith(".png")]

    def select_background(self):
        bg = CaptchaUtils.random_choice_from(self._bgs)
        return bg

    def select_bg_custom_fn(self):
        fn = None
        if self._bg_custom_fns:
            fn = CaptchaUtils.random_choice_from(self._bg_custom_fns)

        return fn

    def select_text(self):
        if len(self._texts) == 1:
            # 经过init_text后，如果还是只有一个元素，则认为这个元素就是可显示在验证中所有字符的集合
            return ''.join([CaptchaUtils.random_choice_from(self._texts[0]) for i in range(self._num)])
        elif len(self._texts) > 1:
            # 否则，每个元素对应一张验证码的内容
            return CaptchaUtils.random_choice_from(self._texts).strip("\n")

    def generate_captcha(self, text=None, bg=None, bg_custom_fn=None, specific_chars=None):
        text = text or self.select_text()
        bg = bg or self.select_background()
        bg_custom_fn = bg_custom_fn or self.select_bg_custom_fn()
        return Captcha(text=text, bg=bg, char_custom_fns=self._char_custom_fns,
                       bg_custom_fn=bg_custom_fn, specific_chars=specific_chars, **self._kwargs)

        # def generate_captcha(self):
        #     text = self.select_text()
        #     bg = self.select_background()
        #     return Captcha(text, bg, **self._kwargs)
