# -*- coding:utf-8 -*-
import sys
# print sys.path

from splinter.browser import Browser

url = 'https://kyfw.12306.cn/otn/leftTicket/init'
b = Browser(driver_name='chrome')
b.visit(url)






#b.find_by_text(u"登录").click()
#b.fill("loginUserDTO.user_name", '37246181@qq.com')
#b.fill("userDTO.password", 'jinling123')
