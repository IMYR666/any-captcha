# any-captcha
generate any type of captcha with one config.
## CONFIG参数说明
* <code>texts</code>:  
  类型：字符串数组  
  说明：验证码上可显示的所有字符的集合，如果：  
   1. 数组长度大于1，每个元素能且只能是普通字符串（非文件或文件夹路径），且每个元素作为整体随机的显示在验证码中，此时<code>num</code>参数失效，每张验证码的字符个数由当前元素长度决定；  
   2. 数组长度等于1，每个元素可以是： 
       > 文件路径：将文件中的每一行作为一个元素存储到数组中，然后按照1.处理；  
    普通字符串：则随机选取<code>num</code>个字符显示在每个验证码中。  
     注：暂不支持文件夹路径。 
* <code>fonts</code>:  
  类型：字符串数组
  说明：验证码字体文件（.ttf或.ttc,不区分大小写）路径的集合，如果：  
     1. 数组长度大于1，每个元素能且只能是字体文件的路径；
     2. 数组长度等于1，可以是单个字体文件的路径，或者存放字体的文件夹路径
* <code>sizes</code>:  
  类型：整型数组  
  说明：验证码中字号大小的集合  
  
* <code>colors</code>:  
  类型：整型数组  
  说明：验证码中字体颜色的集合，单个元素的值为颜色的6位16进制，以"0x"开头
  
* <code>bgs</code>:  
  类型：字符串数组
  说明：验证码的背景图片或者颜色的集合，如果：
     1. 数组长度大于1，每个元素可以是<code>【单张背景图片路径，单个背景颜色（格式同<code>colors</code>参数）】</code>中的一个；
     2. 数组长度等于1，此元素可以是<code>【单张背景图片路径，单个背景颜色，存放多张背景图片的文件夹路径，存放多个背景颜色值的txt文件路径（每行一个颜色值）】</code>中的一个；  
     
* <code>rotate</code>:
  类型：整型  
  说明：验证码中单个字符可旋转角度的值，旋转角度的范围[-<code>rotate</code>, <code>rotate</code>],每次随机取值
  
* <code>num</code>:  
  类型：整型  
  说明：验证码显示的字符个数，具体参见<code>texts</code>参数
* <code>dot</code>:  
  类型：整型  
  说明：验证码中随机噪点的个数，0不显示噪点
* <code>curve</code>:  
  类型：整型  
  说明：验证码中随机干扰线的个数，0不显示干扰线
* <code>width</code>:  
  类型：整型  
  说明：验证码的宽度
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
  类型：浮点型  
  说明：验证码中字符可选的透明度集合，取值范围[0.0,10.0]

注：以上参数都可以被<code>CaptchaFactory.generate_captcha()</code>方法中的相关参数覆盖，即可以动态指定每一个参数，适用于需要遍历所有字符的情况。
