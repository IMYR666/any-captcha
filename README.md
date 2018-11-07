update markdown and demo code
  
* <code>height</code>:  
  类型：整型  
  说明：验证码的高度  
  
* <code>align</code>:  
  类型：整型  
  说明：验证码的对齐方式，取值1或2, 其中1为左对齐，2为两端对齐  
  
* <code>offset_ver</code>:  
  类型：整型  
  说明：验证码中单个字符对象的垂直偏移量，默认（0）垂直居中，如果 <code>offset_ver > 0</code>, 随机从[-<code>offset_ver</code>, <code>offset_ver</code>]中选取一个偏移量  
  
* <code>offset_hor</code>:  
  类型：整型  
  说明：验证码中单个字符对象的水平偏移量，默认（0）与前一个相接，如果 <code>offset_hor > 0</code>, 随机从[-<code>offset_hor</code>, <code>offset_hor</code>]中选取一个偏移量  
  
* <code>char_tran</code>:    
  类型：浮点型数组  
  说明：验证码中字符可选的透明度集合，单个元素取值范围[0.0,10.0]  

注：以上参数都可以被<code>CaptchaFactory.generate_captcha()</code>方法中的相关参数覆盖，即可以动态指定每一个参数，适用于需要遍历所有字符的情况。
   

## 样例代码
* 目标验证码：http://www.58guakao.com/user/487549.html
* config:
```json
{
  "texts": [
    "0123456789"
  ],
  "fonts": [
    "resources/font/CalibriL.ttf"
  ],
  "sizes": [
    28
  ],
  "colors": [
    "0xff0000"
  ],
  "bgs": [
    "0xfef6f6",
    "0xfefdf9"
  ],
  "rotate": 0,
  "num": 11,
  "dot": 0,
  "curve": 0,
  "width": 167,
  "height": 35,
  "align": 1,
  "offset_ver": 0,
  "offset_hor": 0,
  "char_tran": [
    5.97
  ]
}
```
* main code:
```python
def main():
    project_name = "58gua_kao"
    with open("configs/%s.json" % project_name, encoding="utf-8") as fp:
        demo_config = json.load(fp)

    demo_factory = CaptchaFactory(char_custom_fns=[char_custom_fn], bg_custom_fns=[bg_custom_fn], **demo_config)
    index = 10
    while index:
        # text = generate_phone_number(index)
        text = generate_mobile_number(index)

        captcha = demo_factory.generate_captcha(text=text)
        captcha.save("output/%s/%s.jpg" % (project_name, captcha.text))
        print(captcha.text, captcha.num)

        index -= 1
```
char_custom_fns：如果对于单个字符有其他自定义操作，比如形变，膨胀腐蚀等，可以通过此参数传入回调函数，支持多个回调函数随机调用。  
bg_custom_fns：如果对于验证码背景有其他自定义操作，比如高斯模糊、指定样式的噪点或干扰线，可以通过此参数传入回调函数，支持多个回调函数随机调用
## 效果展示  

原始验证码 | 生成验证码     
| :-----: | :-----: |    
| ![58_o](resources/markdown/58.gif) | ![58_g](resources/markdown/138-13049954.jpg) |  
| ![icp_o](resources/markdown/icp.jpg) | ![icp_g](resources/markdown/6NJ6FU.jpg) |  
| ![jd_o](resources/markdown/jd.jpg) | ![jd_g](resources/markdown/9nEL.jpg) |  
| ![jd_o](resources/markdown/jy_o.jpg) | ![jd_g](resources/markdown/jy_g.jpg) |  

## 高级功能
* 字符位置：  
可以通过<code>Captcha.char_pos()</code>方法获取单个字符在验证码中的位置信息，返回一个四元组(x,y,w,h)，分别表示左上角x坐标,y坐标,宽,高，适用于物体检测，文字定位等问题。  
样例：
```python
captcha = demo_factory.generate_captcha()
char_pos = captcha.char_pos
    width = captcha.width
    height = captcha.height
    with open(os.path.join(output_path, txt_out), "w", encoding="utf-8") as fp:
        for pos in char_pos:
            x, y, w, h = pos
            # 转化为中心点的坐标
            # x = (x + w / 2) * 1.0 / width
            # y = (y + h / 2) * 1.0 / height
```


## TODO  


