# -*- coding: utf-8 -*-
from config import *
from action_mail import *
class GoogleSearch(MethodView):
	def get(self):
        	return render_template('google_search.html')
class DashboardMail(MethodView):
	def post(self):
        	mail=MailMethod()
		to="core-editors@googlegroups.com"
               # to='bryan@infoq.com;arthur@infoq.com'
                subject=u'InfoQ中文站Dashboard  %s'%(str(datetime.today())[0:10])
                content=Clue_Pre%('','中文站Dashboard')
                content+='''<a target="_blank" href="http://infoqhelp.sinaapp.com/countstaticsmail" style="margin-left:10px;display:inline-block;padding:2px 5px;background-color:#d44b38;color:#fff;font-size:13px;font-weight:bold;border-radius:2px;border:solid 1px #c43b28;white-space:nowrap;text-decoration:none">查看</a>'''
                content+=Clue_End2
                mail._send_default(to,subject,content)
                return 'ok'
class SmileMail(MethodView):
	def post(self):
        	mail=MailMethod()
                to='staff-infoqchina@googlegroups.com'
                #to='arthur@infoq.com'
                subject=u'InfoQ中文站工作周报  %s'%(str(datetime.today())[0:10])
                content=u"""亲^o^，请分享和总结本周的工作哦，每日精进，我们一直在路上……<br/><br/>
<p><strong>格式参考：</strong>本周主要工作进展（结合项目）、每日精进（日常工作改进的地方）、遇到的问题、下周工作计划、核心价值观事例</p>"""
                mail._send_default(to,subject,content)
                return 'ok'
class BryanMail(MethodView):
	def post(self):
        	mail=MailMethod()
                #to='arthur@infoq.com'
                to='bryan@infoq.com'
                subject=u'设置内容领域'
                content=u"""Bryan:<br/>该设置内容所属的领域啦，猛击<a href="http://infoqhelp.sinaapp.com/setmaincatall">这里</a>"""
                mail._send_default(to,subject,content)
                return 'ok'
class InvoiceMail(MethodView):
	def post(self):
        	mail=MailMethod()
                to='staff-infoqchina@googlegroups.com'
                subject=u'请25日之前提交%s月报销票据'%(str(datetime.today().month))
                content=u'Hi All:<br/>请大家配合Linda的工作，在本月25日之前提交需要报销的票据。逾期不能提交者，请向Kevin提出书面申请，详细解释理由，否则不予报销，请大家理解。<br/><a href="http://gege.baihui.com/open.do?docid=102919000000002015">点此提交</a>invoice'
                mail._send_default(to,subject,content)
                return 'ok'
                
                
class DutyMail(MethodView):
	def get(self):
        	mail=MailMethod()
                to='jessie@c4media.com;arthur@infoq.com'
                subject=u'值班时间安排'
                content=u"""
                	
                        <html><head></head><body>Hi All:<br/>请各部门的同学对照以下表格实行值班，值班期间，团队所有成员均需统一到单位办公。
<br/><table id="pageHeaderId" border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td>
<hr class="hr" />
</td>
</tr>
<tr>
<td valign="top"><br /></td>
</tr>
</tbody>
</table>
<div id="subBC" class="zwPageCont"><span class="normtext" id="contentArea"> 
<table style="width: 100%;" rules="all" frame="box" border="1" cellpadding="7">
<tbody>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><br /></td>
<td style="text-align: center; width: 20%;" valign="top"><b>编辑部</b></td>
<td style="text-align: center; width: 20%;" valign="top"><b>销售部</b></td>
<td style="text-align: center; width: 20%;" valign="top"><b>活动部</b></td>
<td style="text-align: center; width: 20%;" valign="top"><b>商务部</b></td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>June</b></td>
<td style="text-align: center; width: 20%;" valign="top">05&amp;7</td>
<td style="text-align: center; width: 20%;" valign="top">12&amp;14</td>
<td style="text-align: center; width: 20%;" valign="top">19&amp;21</td>
<td style="text-align: center; width: 20%;" valign="top">25&amp;28</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>July</b></td>
<td style="text-align: center; width: 20%;" valign="top">03&amp;05</td>
<td style="text-align: center; width: 20%;" valign="top">10&amp;12</td>
<td style="text-align: center; width: 20%;" valign="top">17&amp;19</td>
<td style="text-align: center; width: 20%;" valign="top">24&amp;26</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>Aug</b></td>
<td style="text-align: center; width: 20%;" valign="top">*31&amp;02 &nbsp; &nbsp; &nbsp;</td>
<td style="text-align: center; width: 20%;" valign="top">06&amp;09</td>
<td style="text-align: center; width: 20%;" valign="top">13&amp;16</td>
<td style="text-align: center; width: 20%;" valign="top">20&amp;23</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>Sep</b></td>
<td style="text-align: center; width: 20%;" valign="top">*27&amp;*30</td>
<td style="text-align: center; width: 20%;" valign="top">03&amp;06</td>
<td style="text-align: center; width: 20%;" valign="top">10&amp;13</td>
<td style="text-align: center; width: 20%;" valign="top">17&amp;20</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>Oct</b></td>
<td style="text-align: center; width: 20%;" valign="top">*24&amp;*27</td>
<td style="text-align: center; width: 20%;" valign="top">9&amp;11</td>
<td style="text-align: center; width: 20%;" valign="top">16&amp;18</td>
<td style="text-align: center; width: 20%;" valign="top">23&amp;25</td>
</tr>
</tbody>
</table>
<br />
<div><font class="Apple-style-span" color="#ff0000">备注：*标记表示顺延上个月 &nbsp; 如Aug 第一列里的*31 &nbsp;实际指的是July 31</font></div>
</span></div></body></html>
                
                """
                mail._send_default(to,subject,content)
                return 'ok'
        def post(self):
        	mail=MailMethod()
                to='staff-infoqchina@googlegroups.com'
                subject=u'值班时间安排'
                content=u"""
                	
                        <html><head></head><body>Hi All:<br/>请各部门的同学对照以下表格实行值班，值班期间，团队所有成员均需统一到单位办公。
<br/><table id="pageHeaderId" border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td>
<hr class="hr" />
</td>
</tr>
<tr>
<td valign="top"><br /></td>
</tr>
</tbody>
</table>
<div id="subBC" class="zwPageCont"><span class="normtext" id="contentArea"> 
<table style="width: 100%;" rules="all" frame="box" border="1" cellpadding="7">
<tbody>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><br /></td>
<td style="text-align: center; width: 20%;" valign="top"><b>编辑部</b></td>
<td style="text-align: center; width: 20%;" valign="top"><b>销售部</b></td>
<td style="text-align: center; width: 20%;" valign="top"><b>活动部</b></td>
<td style="text-align: center; width: 20%;" valign="top"><b>商务部</b></td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>June</b></td>
<td style="text-align: center; width: 20%;" valign="top">05&amp;7</td>
<td style="text-align: center; width: 20%;" valign="top">12&amp;14</td>
<td style="text-align: center; width: 20%;" valign="top">19&amp;21</td>
<td style="text-align: center; width: 20%;" valign="top">25&amp;28</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>July</b></td>
<td style="text-align: center; width: 20%;" valign="top">03&amp;05</td>
<td style="text-align: center; width: 20%;" valign="top">10&amp;12</td>
<td style="text-align: center; width: 20%;" valign="top">17&amp;19</td>
<td style="text-align: center; width: 20%;" valign="top">24&amp;26</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>Aug</b></td>
<td style="text-align: center; width: 20%;" valign="top">*31&amp;02 &nbsp; &nbsp; &nbsp;</td>
<td style="text-align: center; width: 20%;" valign="top">06&amp;09</td>
<td style="text-align: center; width: 20%;" valign="top">13&amp;16</td>
<td style="text-align: center; width: 20%;" valign="top">20&amp;23</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>Sep</b></td>
<td style="text-align: center; width: 20%;" valign="top">*27&amp;*30</td>
<td style="text-align: center; width: 20%;" valign="top">03&amp;06</td>
<td style="text-align: center; width: 20%;" valign="top">10&amp;13</td>
<td style="text-align: center; width: 20%;" valign="top">17&amp;20</td>
</tr>
<tr>
<td style="text-align: center; width: 20%;" valign="top"><b>Oct</b></td>
<td style="text-align: center; width: 20%;" valign="top">*24&amp;*27</td>
<td style="text-align: center; width: 20%;" valign="top">9&amp;11</td>
<td style="text-align: center; width: 20%;" valign="top">16&amp;18</td>
<td style="text-align: center; width: 20%;" valign="top">23&amp;25</td>
</tr>
</tbody>
</table>
<br />
<div><font class="Apple-style-span" color="#ff0000">备注：*标记表示顺延上个月 &nbsp; 如Aug 第一列里的*31 &nbsp;实际指的是July 31</font></div>
</span></div></body></html>
                
                """
                mail._send_default(to,subject,content)
                return 'ok'