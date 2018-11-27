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

