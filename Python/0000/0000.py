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