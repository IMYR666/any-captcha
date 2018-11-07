# coding: utf-8

from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from model.utils import CaptchaUtils


class Char(object):
    def __init__(self, char='A', color="0x000000", font="consola.ttf", size=40, draw=None,
                 rotate=0, position_x=None, position_y=None, char_tran=5.97, custom_fn=None):
        # 字符的文字
        self._char_text = char
        # 字符的颜色
        self._color = color
        # 字符的字体
        self._font = font
        # 字符字体的大小
        self._fsize = size
        self._draw = draw
        # 字符的宽度，根据字符图片旋转，自定义处理后自动算出，不要手动设置
        self._width = None
        # 字符的高度，根据字符图片旋转，自定义处理后自动算出，不要手动设置
        self._height = None
        # 字符在背景图中的x坐标
        self._position_x = position_x
        # 字符在背景图中的y坐标
        self._position_y = position_y
        # 字符的旋转角度
        self._rotate = rotate
        # 字符的自定义函数
        self._custom_fn = custom_fn
        # 字符的图片对象
        self._char_image = None
        self._char_image = self.char
        # 字符的图片透明度
        self._char_tran = char_tran
        self._table = []
        self._table = self.table
        self._mask = self._char_image.convert('L').point(self.table)

    @property
    def table(self):
        if self._table:
            return self._table
        else:
            for i in range(256):
                self._table.append(i * self._char_tran)
            return self._table

    def generate_true_font(self):
        return truetype(self._font, self._fsize)

    def create_character(self):
        font = self.generate_true_font()
        w, h = self._draw.textsize(self._char_text, font=font)

        self._char_image = Image.new('RGB', (w, h), 0)  # (255, 255, 255)
        color = CaptchaUtils.get_rgb(self._color)
        Draw(self._char_image).text((0, 0), self._char_text, font=font, fill=color)
        # self._char_image.show()
        self._char_image = self._char_image.rotate(self._rotate, Image.BILINEAR, expand=1)
        self._char_image = self._char_image.crop(self._char_image.getbbox())
        if self._custom_fn:
            tmp = self._char_image
            self._char_image = self._custom_fn(tmp)
            self._char_image = self._char_image.crop(self._char_image.getbbox())

        self._width = self._char_image.size[0]
        self._height = self._char_image.size[1]

    @property
    def char(self):
        if self._char_image is None:
            self.create_character()

        return self._char_image

    @property
    def font(self):
        return self._font

    @property
    def char_text(self):
        return self._char_text

    @property
    def color(self):
        return self._color

    @property
    def rotate(self):
        return self._rotate

    @property
    def fsize(self):
        return self._fsize

    @property
    def position_x(self):
        return self._position_x

    @property
    def position_y(self):
        return self._position_y

    @property
    def mask(self):
        return self._mask

    def set_x(self, pos):
        self._position_x = pos

    def set_y(self, pos):
        self._position_y = pos
