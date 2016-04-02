# -*- coding:utf-8 -*-
VERSION = r'2016/04/02'
# 配置中心
URL = "http://wg.suda.edu.cn/indexn.aspx"
STUDENT_ID = 'XXXXXXXXXXXXXXXXXXXX'
STUDENT_PASSWORD = 'XXXXXXXXXXXXXXXXXXXX'
'''
Created on 2016年4月2日
@author: XenoAmess
'''
import urllib.parse
import urllib.request
import time

def get_html(url):
    '''首先通讯，获得一个html字符串，返回这个字符串'''
    html_byte = urllib.request.urlopen(url).read()
    html_str = str(html_byte, "utf-8")
    return html_str
    
def txt_wrap_by(start_str, end_str, html_str):
    '''取出字符串html_str中的，被start_str与end_str包绕的字符串'''
    start = html_str.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html_str.find(end_str, start)
        if end >= 0:
            return html_str[start:end].strip()

def read_html_for_money(html_str):
    '''读取拿到的html，返回钱数'''
    
    reg__L = r"</font><br/><br/><font color='#000'>您的帐户余额是<font color='#ff0000'><b>"
    reg__R = r"</b></font>元。</font><br><br>"

    money = txt_wrap_by(reg__L, reg__R, html_str)
    return money
    
def read_html_for_keys(html_str):
    '''读取拿到的html，返回两个关键值'''
    
    reg__VIEWSTATE = r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="'
    reg__EVENTVALIDATION = r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="'
    reg__right = r'" />'
    
    viewstate = txt_wrap_by(reg__VIEWSTATE, reg__right, html_str)
    eventvalidation = txt_wrap_by(reg__EVENTVALIDATION, reg__right, html_str)
    
    return viewstate, eventvalidation
# file_input = open('data.txt')
# html_str = file_input.read()
# file_input.close()
# read_html(html_str)

def reget_html(url, string_student_id, string_student_password, VIEWSTATE, EVENTVALIDATION):  
    '''再次向html通信'''
    search = urllib.parse.urlencode([
        ('__EVENTTARGET', ''),
        ('__EVENTARGUMENT', ''),
        ('__VIEWSTATE', VIEWSTATE),
        ('__EVENTVALIDATION', EVENTVALIDATION),
        ('TextBox1', string_student_id),
        ('TextBox2', string_student_password),
        ('nw', 'RadioButton2'),
        ('tm', 'RadioButton8'),
        ('Button1', '登录网关'),
    ])
    search = bytes(search, encoding="utf8")
    html_byte = urllib.request.urlopen(url, search).read()
    html_str = str(html_byte, "utf-8")
    return html_str

def output_to_file(file_name_str, file_str):
    file_output = open(file_name_str, 'w')
    file_output.write(file_str)
    file_output.close()

def main():
    html_str = get_html(URL)
    output_to_file('before.html', html_str)
    VIEWSTATE, EVENTVALIDATION = read_html_for_keys(html_str)
    html_str = reget_html(URL, STUDENT_ID, STUDENT_PASSWORD, VIEWSTATE, EVENTVALIDATION)
    output_to_file('after.html', html_str)
    
    print(time.strftime("%c"))
    
    money = read_html_for_money(html_str)
    if(money != None):
        print('登录成功。您的账户余额为' + money + '元。')
    else:
        print('请检查您是否已登录。若现在仍无网络连接，则意味着本程序已失效。')
        
def runforever():
    '''每隔十分钟自动登录一次'''
    while(1):
        main()
        time.sleep(10 * 60)


if (__name__ == "__main__"):
    
    print('苏大网关自动登录器')
    print()
    print('版本:')
    print(VERSION)
    print()
    print('用户ID:')
    print(STUDENT_ID)
    print()
    print('用户密码:')
    print(STUDENT_PASSWORD)
    print()
    print('网关地址:')
    print(URL)
    print()
    print('作者:')
    print('XenoAmess')
    print()
    print('说明:')
    print(r'由于网关似乎经常掉线，所以该程序每10分钟自动登录一次。只需要最小化以后挂在那里不用管就行了。当然了虽然选哪个按钮都是2小时以后就退出了，不过我还是模拟的选的10小时的按钮。如果您不需要多次的话，请翻源码把下一行的runforever()改成main()就行了。')
    
    runforever()
