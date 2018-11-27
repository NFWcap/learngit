## Description

- Yixiaohan/show-me-the-code Python 练习册，每天一个小程序 第0001题
- 做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用**生成激活码**（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？ 

## Notes

- 先思考需要生成的激活码的组成格式，这里我们采用了xxxx-xxxx-xxxx-xxxx的格式，且采用大写字母和数字混合的方式

- 生成主要使用`random`库中的

  - `sample`函数：random.sample(sequence, k)

    \#从指定序列中随机获取指定长度的片断并随机排列。注意：sample函数不会修改原有序列。

  - 和`choice`函数：random.choice(sequence)

    \#random.choice从序列中获取一个随机元素。其函数原型为：random.choice(sequence)。

- 使用`join`函数进行连接：

  - 语法：  `' A ' . join ( B )`

    参数说明
    A：分隔符。可以为空或者空格甚至是数字
    B：要连接的元素序列、字符串、元组、字典
    上面的语法即：以 A 作为分隔符，将 B 所有的元素合并成一个新的字符串

##  Data

- **[random模块介绍](https://www.cnblogs.com/liangmingshen/p/8909376.html)**



## Code

```
import random
list1=[]
cdk_list = []
cdk = []
code_list=[]

def activation_code_generator(num):

    '''
    生成所需要的字典
    '''
    for x in range(1,10):
        list1.append(x)

    for i in range(65,91):
        a = str(chr(i))
        list1.append(a)

    '''
    随机抽取四个字符
    '''
    for j in range(0,num*4):
        temp = random.sample(list1,4)

        # list中包含数字，不能直接转换为字符串，
        # 遍历list元素，把他转化为字符串
        # 将每个单独的字符进行拼接
        str1 = "".join('%s' %id for id in temp)
        cdk.append(str1)
    list_temp = []

    #每4个使用- 进行连接

    for k in range(0,num*4):
        if k != 0 and k % 4 == 0:
            str2 = "-".join('%s' %id for id in list_temp)
            code_list.append(str2)
            list_temp = []
        list_temp.append(cdk[k])

    return code_list

def get_code(num):
    for x in range(num):
        a = random.choice(code_list)
        print(a)

def main():
    num1  = input('请输入需要的激活码数量:')
    num = int(num1)
    activation_code_generator(num)
    get_code(num)


main()

'''主要使用了random库和join函数'''


```

