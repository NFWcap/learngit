## Description
- Yixiaohan/show-me-the-code Python 练习册，每天一个小程序 第0000题
- 将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。 类似于图中效果

![这里写图片描述](https://camo.githubusercontent.com/d518d3929e4054ce2f9183b23e52908da7e5632d/687474703a2f2f692e696d6775722e636f6d2f736732646b75592e706e673f31) 

## Notes

- 主要使用了PIL库，以及PIL库中的`Image`,`ImageDraw`,`ImageFont`模块
- ImageDraw.Draw()函数会创建一个用来对image进行操作的对象，对所有即将使用ImageDraw中操作的图片都要先进行对象的创建
- 字体要用已存在的字体
- 注意打开文件的路径
- 调用Image.open()打开image之后，记得要再调用close()将其关闭，不然会一直占用内存资源。
-  注意写字位置的坐标，如果超过image的坐标范围就看不见了

## Data

- **[ImageDraw模块介绍](https://blog.csdn.net/icamera0/article/details/50747084)**



## Code

```
import PIL
from PIL import Image,ImageDraw,ImageFont

def addNumToImg(img):

    # ImageDraw.Draw()函数会创建一个用来对image进行操作的对象
    # 对所有即将使用ImageDraw中操作的图片都要先进行对象的创建
    drawimg= ImageDraw.Draw(img)

    #设置好字体和字号大小
    font = ImageFont.truetype("arial.ttf",40)

    #获取图片属性，大小
    w,h = img.size

    #添加数字内容（其中第一个参数是位置，第二个是添加的内容，第三个表示颜色，第四个是字体）
    #其中（255，0，0）表示完全红色，三个数分别代表red，green，blue
    drawimg.text((w-200,100),"99+",(255,0,0),font)
    img.save("modified.jpg","jpeg")

    modified_img = Image.open("modified.jpg")
    modified_img.show()


img = Image.open("qq.jpg")
addNumToImg(img)

#对每个打开的流都要关闭，防止占用内存
img.close()
```

