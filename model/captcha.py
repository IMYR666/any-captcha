# coding: utf-8
import os
import random

import re
from PIL import Image
from PIL.ImageDraw import Draw
from model.utils import CaptchaUtils
from model.char import Char


class Captcha(object):
    def __init__(self, text, bg, char_custom_fns=None, bg_custom_fn=None, specific_chars=None, **kwargs):
        self._kwargs = kwargs
        # 验证码上显示的文本内容
        self._text = text
        # 验证码的背景，图片路径或者颜色字符串（e.g.:0xffffff）
        self._background = bg
        # 验证码文本长度
        self._num = len(self._text)
        # 验证码中所有的字符对象, [anycaptcha.char.Char] 类型
        self._chars = []
        # 验证码中所有的字符的位置信息，4-tuple(e.g.(0,0,25,30)),分别表示左上角点x坐标,y坐标,宽,高
        self._char_pos = []

        # 验证码背景处理的自定义函数
        self._bg_custom_fn = bg_custom_fn

        # 验证码指定字符的详细信息，相关配置参见"configs/char/specific_chars.json"
        self._specific_chars = specific_chars

        # 验证码噪点的个数
        self._dot = self._kwargs.get("dot", 0)

        # 验证码干扰线的个数
        self._curve = self._kwargs.get("curve", 0)

        # 验证码的宽
        self._width = self._kwargs.get("width", 60)

        # 验证码的高
        self._height = self._kwargs.get("height", 200)

        # 验证码中单个字符对象的垂直偏移量，默认（0）垂直居中，if > 0, 随机从（-_off_ver，_off_ver）中选取一个
        self._off_ver = self._kwargs.get("offset_ver", 0)

        # 验证码中单个字符对象的水平偏移量，默认（0）紧跟上个字符，if > 0, 随机从（-_off_hor，_off_hor）中选取一个
        self._off_hor = self._kwargs.get("offset_hor", 0)

        # 验证码中单个字符对象的轮廓线的颜色，如果为空，则不显示
        self._outline_color = self._kwargs.get("outline_color", None)

        # 验证码中字符的对齐方式，1：左对齐；2：两端对齐
        self._align = self._kwargs.get("align", 2)

        # 验证码中字符可选的字体集合
        self._char_fonts = self._kwargs.get("fonts", ["consola.ttf"])
        # 验证码中字符可选的字体大小集合
        self._char_sizes = self._kwargs.get("sizes", [38, 40, 42])
        # 验证码中字符可选的字体颜色集合
        self._char_colors = self._kwargs.get("colors", ["0xffffff"])
        # 验证码中字符可选的旋转角度集合(-_char_rotate,_char_rotate)
        self._char_rotate = self._kwargs.get("rotate", 0)
        # 验证码中字符可选的透明度集合(0-100)
        self._char_tran = self._kwargs.get("char_tran", [5.97])
        # 验证码处理单个字符的自定义函数集合
        self._char_custom_fns = char_custom_fns

        self._captcha = None
        self.init_font()
        self._captcha = self.captcha

    def init_font_size(self):
        CaptchaUtils.random_choice_from(self._char_sizes)

    def init_captcha(self):
        tmp_captcha = None
        if os.path.isfile(self._background):
            tmp_captcha = Image.open(self._background).resize((self._width, self._height))
        else:
            bg = CaptchaUtils.get_rgb(self._background)
            tmp_captcha = Image.new('RGB', (self._width, self._height), bg)

        if self._bg_custom_fn:
            tmp_captcha = self._bg_custom_fn(tmp_captcha)

        return tmp_captcha

    def init_font(self):
        if len(self._char_fonts) == 1:
            unknown_string = self._char_fonts[0]
            if os.path.isdir(unknown_string):
                files = os.listdir(unknown_string)

                self._char_fonts = [os.path.join(unknown_string, file) for file in files if
                                    file.lower().endswith(".ttf") or file.lower().endswith(".ttc")]

        for _char_font in self._char_fonts:
            if not os.path.isfile(_char_font):
                raise FileNotFoundError("this font connot be found. font path:%s" % _char_font)

    def select_rotate(self):
        rotate = random.uniform(-self._char_rotate, self._char_rotate)

        return rotate

    def select_char_custom_fns(self):
        fn = None
        if self._char_custom_fns:
            fn = CaptchaUtils.random_choice_from(self._char_custom_fns)

        return fn

    def select_font(self):
        font = CaptchaUtils.random_choice_from(self._char_fonts)

        return font

    def select_size(self):
        size = CaptchaUtils.random_choice_from(self._char_sizes)

        return size

    def select_char_tran(self):
        char_tran = CaptchaUtils.random_choice_from(self._char_tran)

        return char_tran

    def select_color(self):
        color = CaptchaUtils.random_choice_from(self._char_colors)

        return color

    def draw_noise_dot(self, color="0x484848", width=3, number=30):
        while number:
            CaptchaUtils.draw_dot(self._captcha, color=CaptchaUtils.get_rgb(color), width=width)
            number -= 1

    def draw_noise_curve(self, color="0x484848", number=4, width=3, type="line"):
        points = [CaptchaUtils.random_point(self._width, self._height) for i in range(number + 1)]
        if type == "line":
            for idx in range(len(points) - 1):
                CaptchaUtils.draw_line(self._captcha, points[idx], points[idx + 1], CaptchaUtils.get_rgb(color), width)
        elif type == "curve":
            pass
        # CaptchaUtils.draw_curve()
        else:
            pass

    def get_actual_x(self, except_x, im_width):
        act = except_x + random.randint(-self._off_hor, self._off_hor)

        if act + im_width > self._width - 2:
            return self._width - im_width - 2
        elif act < 2:
            return 2
        else:
            return act

    def get_actual_y(self, except_y, h):
        act = except_y + random.randint(-self._off_ver, self._off_ver)

        if act + h > self._height - 2:
            return self._height - h - 2
        elif act < 2:
            return 2
        else:
            return act

    def joint_image(self):
        average = int(self._width / self._num)
        except_x = 0

        for char in self._chars:
            _char = char.char
            # _char.show()
            w, h = _char.size
            except_y = int((self._height - h) / 2)

            if char.position_x is None:
                char.set_x(self.get_actual_x(except_x, w))
            if char.position_y is None:
                char.set_y(self.get_actual_y(except_y, h))

            self._captcha.paste(_char, (char.position_x, char.position_y), char.mask)
            # self._captcha.show()
            self._char_pos.append((char.position_x, char.position_y, w, h))

            if self._outline_color:
                color = CaptchaUtils.get_rgb(self._outline_color)
                self.draw_outline(char.position_x, char.position_y, w, h, color)
            # 左对齐
            if self._align == 1:
                except_x += _char.width
            else:  # 两端对齐
                except_x += average

    def draw_outline(self, actual_x, actual_y, w, h, color):
        CaptchaUtils.draw_rectangle(self._captcha, (actual_x, actual_y, w, h), color)

    def create_captcha(self):
        specific = [{}] * self._num
        if self._specific_chars:
            specific = self._specific_chars
            [specific.append({}) for i in range(self._num - len(specific)) if self._num - len(specific) > 0]
        act_text = []
        for i in range(self._num):
            draw = Draw(self._captcha)
            char = specific[i].get("char", self._text[i])
            color = specific[i].get("color", self.select_color())
            font = specific[i].get("font", self.select_font())
            size = specific[i].get("size", self.select_size())
            rotate = specific[i].get("rotate", self.select_rotate())
            x = specific[i].get("position_x", None)
            y = specific[i].get("position_y", None)
            fn = specific[i].get("fn", self.select_char_custom_fns())
            char_tran = specific[i].get("char_tran", self.select_char_tran())
            self._chars.append(Char(char=char, color=color, font=font, size=size, draw=draw,
                                    rotate=rotate, position_x=x, position_y=y, char_tran=char_tran, custom_fn=fn))

            act_text.append(char)

        if len(specific) > self._num:
            for i in range(self._num, len(specific)):
                act_text.append(specific[i].get("char", "A"))
                self._chars.append(Char(draw=Draw(self._captcha), **specific[i]))
                self._num += 1

        self._text = "".join(act_text)
        self.joint_image()

        if self._curve:
            self.draw_noise_curve(number=self._curve)
        if self._dot:
            self.draw_noise_dot(number=self._dot)

    def save(self, fp):
        lens = self._captcha.split()
        path = re.findall("(.+/).+", fp)[0]
        if os.path.exists(path) is False:
            os.makedirs(path)

        if fp.lower().endswith("jpg") and len(lens) == 4:
            r, g, b, a = lens
            tmp = Image.merge("RGB", (r, g, b))
            tmp.save(fp, "JPEG")
        else:
            self._captcha.save(fp)

    def show(self):
        self._captcha.show()

    @property
    def captcha(self):
        if self._captcha is None:
            self._captcha = self.init_captcha()
            self.create_captcha()

        return self._captcha

    @property
    def chars(self):
        return self._chars

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def char_pos(self):
        return self._char_pos

    @property
    def background(self):
        return self._background

    @property
    def text(self):
        return self._text

    @property
    def num(self):
        return self._num
