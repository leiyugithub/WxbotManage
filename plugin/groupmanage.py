#!/usr/bin/env python
# coding: utf-8
#####插件说明#####
#监控微信群的  进群、踢出群、群红包、群名称修改等消息并进行处理
import json
import web
import re
import os
import time
import sys

def run(WXBOT,msg,plugin_name):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	try:
		WXBOT.bot_conf[plugin_name]
	except:
		WXBOT.bot_conf[plugin_name] ={
			'switch':True,
			'db_name':'weixin.db',
			'welcome_msg':u'欢迎【%s】入群\n\n进群请改群名片：经纪人编号-姓名\n例：007-詹姆斯邦德（姓名）\n\n一车购，互联网汽车代购专家！\n找我低价购车，'
						  u'从此买车无忧！\n推荐朋友购车，人情佣金两不误\n寻车问价@一车购李军翼  其他问题@群主大大\n'
						  u'准户买车填写http://cn.mikecrm.com/L1PT5wS，半个工作日内工作人员会在群内反馈信息文明交流，禁发广告。',
			'switch_allow_change_gname':False,
			'admin_account_list': [u'Running'] , # 有踢人权限的账号列表
			'alowgroups': [u'机器人',u'一车购经纪人•全国102群']
		}
		return
	#相关日志查看data中的weixin数据库！！
	web_db  			=  web.database(dbn="sqlite", db=os.path.join(os.getcwd(),'data',WXBOT.bot_conf[plugin_name]['db_name']))   #只是示例！！请核自己得数据库对接，修改dbn类型就能对接到自己得数据库中，参考http://webpy.org/cookbook/multidbs.zh-cn
	group_invit_1		=  re.compile(u'(.*?)邀请(.*?)加入了群聊')
	group_invit_2		=  re.compile(u'(.*?)通过扫描(.*?)分享的二维码加入群聊')
	group_delete		=  re.compile(u'(.*?)将(.*?)移出了群聊')
	group_name_change   =  re.compile(u'(.*?)修改群名为(.*?)')

	if msg['user']['name'] in WXBOT.bot_conf[plugin_name]['alowgroups']:
		if WXBOT.bot_conf[plugin_name]['switch'] == True and (msg['msg_type_id'] == 3 and msg['content']['type'] == 0):
			if msg['content']['data'] == u'邀请查询':
				pass  #未处理！！！

			try:
				if msg['content']['detail'][0]['type'] == 'at' and msg['content']['user']['name'] in  WXBOT.bot_conf[plugin_name]['admin_account_list']:
					if msg['content']['desc'] == u'踢':
						print u'[INFO] 收到管理命令：%s-->踢掉-->%s'%(msg['user']['name'],msg['content']['detail'][0]['value'])
						WXBOT.delete_user_from_group(msg['content']['detail'][0]['value'],msg['user']['id'])
			except Exception,e:
				pass

		if WXBOT.bot_conf[plugin_name]['switch'] == True and (msg['msg_type_id'] == 3 and msg['content']['type'] == 12):
			print u'[INFO] 匹配群管控消息成功，%s---->%s'%(msg['user']['name'],msg['content']['data'])
			#对于进群后，改名字的人，不进行统计！而且统计其邀请量的时候也不会统计多！不过 进群-改名-退群-改名-进群-退群 每次都是不同名字进入数据库的情况下还是会多统计，但是邀请数量不会出问题！
			#匹配主动邀请
			result = group_invit_1.findall(msg['content']['data'])
			if len(result)!= 0 :
				 #如果是自己邀请得就pass吧
				if  result[0][0] != u'你':
					for be_inviter in result[0][1].split(u'、'):
						try:
							web_db.insert('group_invt_log',
								group_name  =  msg['user']['name'] ,
								inviter	 =  result[0][0][1:-1],
								be_inviter  =  be_inviter[1:-1],
								invite_time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
								type		=  0
								)
						except Exception,e:
							pass
					WXBOT.get_contact()
					time.sleep(4)
					username = result[0][1]
					username = re.sub(r'<span((?!</?span).)+</span>', '', username).replace('"','')
					WXBOT.send_msg_by_uid(WXBOT.bot_conf[plugin_name]['welcome_msg']%(username),msg['user']['id'])
					#相同的人退出后在入群，不记录日志！
			#匹配二维码扫描入群，人数超过100后就无法扫描入群了
			result = group_invit_2.findall(msg['content']['data'])
			if len(result)!= 0:
				#如果是自己邀请得就pass吧
				if  result[0][0] != u'你':
					for be_inviter in result[0][0].split(u'、'):
						try:
							web_db.insert('group_invt_log',
								group_name  =  msg['user']['name'],
								inviter	 =  result[0][1][1:-1],
								be_inviter  =  be_inviter[1:-1],
								invite_time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
								type		=  1
								)
						except Exception,e:
							pass
			#匹配移除出群消息
			result = group_delete.findall(msg['content']['data'])
			if len(result)!= 0:
				for be_deleter in result[0][0].split(u'、'):
					try:
						 web_db.insert('group_delete_log',
								group_name  =  msg['user']['name'],
								deleter	 =  result[0][1][1:-1],   #被踢得人
								delete_time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
								)
					except Exception,e:
						pass
			#匹配群名称修改消息
			result = group_name_change.findall(msg['content']['data'])
			if len(result)!= 0:
				if  result[0][0] != u'你':
					try:
						#判断一下是否允许修改群名，不允许的话将修改群名回去
						if WXBOT.bot_conf[plugin_name]['switch_allow_change_gname'] == False:
							print u'[INFO] 非管理员修改群名称，将自动修改为原始群名称'
							result = WXBOT.set_group_name(msg['user']['id'],msg['user']['name'])
							print u'修改群名称结果--->%s'%result
						pass
					except Exception,e:
						pass
				WXBOT.get_contact()
			#WXBOT.get_contact()
			return