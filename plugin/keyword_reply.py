#!/usr/bin/env python
# coding: utf-8
#####插件说明#####
#炸群监控插件！！通过匹配消息中的敏感词数量来自动踢出某些群内的捣乱分子
import sys
import re
def run(WXBOT,msg,plugin_name):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	try:
		WXBOT.bot_conf[plugin_name]
	except:
		WXBOT.bot_conf[plugin_name] = {
		    'switch' : True,      #自动回复功能开关
		    'keywords' : {u'买车':u'您好 【%s】，\n准户买车填写http://cn.mikecrm.com/L1PT5wS，半个工作日内工作人员会在群内反馈信息'} ,   #关键字匹配内容
			'alowgroups': [u'机器人',u'一车购经纪人•全国102群']
		}
		return
	if msg['user']['name'] in WXBOT.bot_conf[plugin_name]['alowgroups']:
		if WXBOT.bot_conf[plugin_name]['switch'] == True and (msg['msg_type_id'] == 3 and  msg['content']['type'] == 0):
			print msg
			content = msg['content']['data']
			if WXBOT.bot_conf[plugin_name]['keywords'].has_key(content):
				username = msg['content']['user']['name']
				username = re.sub(r'<span((?!</?span).)+</span>', '', username)
				WXBOT.send_msg_by_uid(WXBOT.bot_conf[plugin_name]['keywords'].get(content)%(username), msg['user']['id'])
			# else:
			# 	content = content.encode('utf-8').upper().replace(' ','')
			# 	jb = jieba_util()
			# 	db = db_utils()
			# 	badgay_message = db.get_car_by_series(jb.getKeyWord(content))
			# 	if badgay_message != '':
			# 		badgay_message = badgay_message + '\n@' + msg['content']['user']['name']
			# 		WXBOT.send_msg_by_uid(badgay_message, msg['user']['id'])