#coding=utf-8
import subprocess
import time
import os
from pywifi import PyWiFi,const,Profile

'''AKM加密方式的list 用来区分加密方式，用来选择连入free或者加密wifi'''
AKM = {0:'NONE',1:'WPA',2:'WPA-PSK',3:'WPA2',4:'WPA2-PSK',5:'UNKNOWN'}

'''信道信息的LIST,超出部分为5g 直接显示'''

Channel = {2412:'1',2417:'2',2422:'3',2427:'4',2432:'5',2437:'6',2442:'7',2447:'8',2452:'9',2457:'10',2462:'11',2467:'12',2472:'13'}
command_release = "dhclient -r"


def interfaces_status(iface):

    '''查看无线网卡的连接状态'''

    iface_name = iface.name()
    print("当前选择无线网卡: %s" %iface_name)
    if iface.status() in [const.IFACE_CONNECTED,const.IFACE_CONNECTING]:
        print('无线网卡 %s 已连接！' % iface_name)
    else:
        print('无线网卡 %s 未连接！' % iface_name)


def interface_disconnect(iface):

    '''断开无线网络连接'''

    iface.disconnect()

    '''释放IP，避免重新连接后不能重新分配IP的问题'''

    subprocess.call(command_release,shell=True) 
    print("已断开...")
    if iface.status() in [const.IFACE_DISCONNECTED,const.IFACE_INACTIVE]:
        print('无线网卡 %s 未连接！' % iface.name())
    else:
        print('无线网卡 %s 已连接！' % iface.name())

		
def connect_ap(iface,wifi_list):

    '''AP连接入口'''

    print('请选择需要连入的AP')
    str1 = int(input('AP序号：'))
    bss = wifi_list[str1-1]

    ''' wifi_list本身就是一个列表'''

    print('AP名称: %s(%s)' %(bss.ssid,bss.bssid))

    '''用于区分连入free和加密wifi'''

    if bss.akm:
        key = input("请输入密码:")
        connect_encrypt(iface,bss,key)
    else:
        connect_open(iface,bss)


def connect_open(iface,bss):

    '''连接开放AP'''

    iface_name = iface.name()
    command_start = "dhclient "+iface_name
    iface.disconnect()
    time.sleep(3)

    '''添加配置文件'''

    profile_info = Profile()
    profile_info.ssid = bss.ssid
    profile_info.akm.append(const.AKM_TYPE_NONE)

    '''删除其他的配置'''

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile_info)
    iface.connect(tmp_profile)
    print("%s 正在连接开放网络 %s(%s)..." %(iface.name(),bss.ssid,bss.bssid))
    time.sleep(5)
    if iface.status() == const.IFACE_CONNECTED:
        print("wifi:%s(%s) 连接成功！" % (bss.ssid,bss.bssid))
        print("正在分配ip地址...")
        subprocess.call(command_release,shell=True)
        subprocess.call(command_start,shell=True)
        print("分配完成！")
    else:
        print("wifi:%s(%s) 连接失败！" % (bss.ssid,bss.bssid))


def connect_encrypt(iface,bss,wifi_password):

    '''连接有密码的AP'''

    iface_name = iface.name()
    command_start = "dhclient "+iface_name
    iface.disconnect()
    time.sleep(3)
    profile_info =  Profile()
    profile_info.ssid = bss.ssid
    profile_info.akm.append(bss.akm[-1]) #akm的list的最新添加的一项
    profile_info.key = wifi_password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile_info)
    iface.connect(tmp_profile)
    print("正在连接...")
    time.sleep(5)
    if iface.status() == const.IFACE_CONNECTED:
        print("wifi:%s(%s) 连接成功！" % (bss.ssid,bss.bssid))
        print("正在分配ip地址...")
        subprocess.call(command_release,shell=True)
        subprocess.call(command_start,shell=True)
        print('分配完成！')
    else:
        print("wifi:%s(%s) 连接失败！" % (bss.ssid,bss.bssid))


def scan_ap(iface):

    '''扫描周围AP'''

    iface.scan()
    time.sleep(3)
    bsses = iface.scan_results()
    return bsses


def show_wifi_list(bsses):

    '''显示AP信息'''

    for i,bss in enumerate(bsses,start=1):
        print('-' *40)
        print('[+]AP的序号:<%s>'%i)
        print('[+]AP的SSID：%s' %bss.ssid)
        print('[+]AP的BSSID：%s' % bss.bssid)
        print('[+]AP的信号强度：%s' %bss.signal)
        if int(bss.freq)>=2412 and int(bss.freq) <= 2472:
            print('[+]AP的信道:%s' %Channel[bss.freq])
        else:
            print('[+]AP的信道:%s' %bss.freq)
        if bss.akm:
            print('[+]AP的认证方式：%s' %AKM[bss.akm[-1]])       
        else:
            print('[+]AP的认证方式: None')
        print('-'* 40)

    
def main():

    try:                                        #捕获异常处理，如果执行脚本不是root，就抛出错误
        if os.getuid() !=0:
            print("[-] Run me as root")
            exit(1)
    except Exception as msg:
        print(msg)
    wifi = PyWiFi()                             #创建并且选择一张网卡
    iface = wifi.interfaces()[0]
    print("当前已选择网卡: %s" %iface.name())
    print('工具启动，正在扫描可用WIFI……')
    wifi_list = scan_ap(iface)                  #输出一个扫描结果wifi表
    print("扫描完成！")
    while(1):
        print('--------------------------')
        print('请选择需要的服务：')
        print('1.显示可用WIFI列表')
        print('2.再次扫描')
        print('3.选择连入WIFI')
        print('4.查看当前网卡状态')
        print('5.断开当前网卡连接')
        print('6.退出程序')
        print('--------------------------')
        choice= input()
        if(choice == '1'):
            show_wifi_list(wifi_list)
        elif(choice == '2'):

            '''再次扫描，得到结果'''

            print('正在扫描……')
            wifi_list = scan_ap(iface)  
            print("扫描完成！")
        elif(choice == '3'):
            connect_ap(iface,wifi_list)
        elif(choice == '4'):
            interfaces_status(iface)
        elif(choice == '5'):
            interface_disconnect(iface)
        elif(choice == '6'):
            exit(0)


if __name__ == '__main__':
    main()

