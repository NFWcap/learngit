from tkinter import *
from tkinter import ttk
import json, urllib.request
import pymysql
from urllib.parse import urlencode

fields =('Basic Money','Exchange Money')
fields1  = ('Number of Money','Rate','Result','Database')
currency = ["人民币","美元","欧元","港币","日元","英镑","澳大利亚元"]
appkey = "cbea01f970765eabe53f4eb73422fdf8"

def put_mysql(entries,entries1):
    db = pymysql.connect("localhost","root","123456","exchange_money",charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO EMPLOYEE(BASIC_MONEY,EXCHANGE_MONEY,ECHANGE_RATE,NUMBER) values (%s,%s,%s,%s)"
    try:
        cursor.execute(sql,[entries['Basic Money'].get(),entries['Exchange Money'].get(),
                            entries1['Rate'].get(),entries1['Number of Money'].get()])
        db.commit()
        entries1['Database'].delete(0,END)
        entries1['Database'].insert(0,'数据已入库')
    except Exception as e:
        print("error:%s" %e)
        db.rollback()
        print("存入失败")

    db.close()
def exchange(entries1): #转换
    num = float(entries1['Number of Money'].get())
    rate = float(entries1['Rate'].get())
    result = num * rate
    entries1['Result'].delete(0, END)
    entries1['Result'].insert(0,result)

def demand(entries,entries1): #查询
    str1 = currency.index(entries['Basic Money'].get())
    str2 = currency.index(entries['Exchange Money'].get())
    if (int(str1) != 0):
        basic_price, basic_name = request1(appkey, str(str1), "GET")
    else:
        basic_price, basic_name = 1, "人民币"
    if (int(str2) != 0):
        exchange_price, exchange_name = request1(appkey, str(str2), "GET")
    else:
        exchange_price, exchange_name = 1, "人民币"
    rate = basic_price/exchange_price
    entries1['Rate'].delete('0',END)
    entries1['Rate'].insert('0',round(rate,4))

def request1(appkey, num1, m="GET"):
    url = "http://web.juhe.cn:8080/finance/exchange/rmbquot"
    params = {
        "key": appkey,  # APP Key
        "type": "",  # 两种格式(0或者1,默认为0)
    }

    params = urlencode(params)
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            # %s %f %d
            #print("%s的汇率为：%f" % (res["result"][0]['data' + num1]['name'], float(res["result"][0]['data' + num1]['fBuyPri']) * 0.01))
            return float(res["result"][0]['data' + num1]['fBuyPri']) * 0.01, res["result"][0]['data' + num1]['name']
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")



def makeform(root,fields):
    entries ={}
    entries1 ={}
    for field in fields:
        row = Frame(root)   #Frame就是屏幕上的一块矩形区域，多是用来作为容器（container）来布局窗体。
        #文本或图像在背景内容区的位置：anchor
        # 可选值为（n,s,w,e,ne,nw,sw,se,center）
        # eswn是东南西北英文的首字母，表示：上北下南左西右东
        lab = Label(row,width = 22,text = field + ":",anchor = 'w')
        com = ttk.Combobox(row, state='readonly')
        com['values'] = (currency)
        com.current(0) #添加默认值为0
        row.pack(side = TOP,fill = X,padx = 5,pady =5)
        lab.pack(side = LEFT)
        com.pack(side = RIGHT,expand = YES,fill =X)
        entries[field] = com

    for field1 in fields1:
        row1 =Frame(root)
        lab = Label(row1, width=22, text=field1 + ": ", anchor='w')
        ent = Entry(row1)
        ent.insert(0, "0")
        row1.pack(side = TOP,fill = X,padx = 5,pady =5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries1[field1] = ent

    return  entries,entries1

if __name__ == '__main__':
    root = Tk()
    root.title('汇率转换器')
    ents,ents1 = makeform(root,fields)
    b1 = Button(root,text = 'Demand',
                command = (lambda e =ents,e1=ents1:demand(e,e1)))
    b1.pack(side = LEFT,padx = 5,pady =5)
    b2 = Button(root, text='Exchange',
                command=(lambda e=ents1: exchange(e)))
    b2.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(root,text = 'Push into Datebases',
                command = (lambda e =ents,e1=ents1:put_mysql(e,e1)))
    b3.pack(side = LEFT,padx =5,pady =5)
    b4 = Button(root,text = 'Quit',command = root.quit)
    b4.pack(side = LEFT,padx = 5,pady = 5)
    root.mainloop()