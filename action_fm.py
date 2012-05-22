# coding: utf-8
import config
from config import *
import os, sys, urllib, urllib2, cookielib, re, json

url_pic_request="http://douban.fm/j/new_captcha"
url_pic ="http://douban.fm/misc/captcha?size=m&id="

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
captcha_id=''
url_login = 'http://douban.fm/j/login'
#alias = raw_input('输入用户名:')
#form_password = raw_input('输入密码:')
#print u'请将如下链接复制到浏览器，获取验证码'
#print "http://douban.fm/misc/captcha?size=m&id=%s" % captcha_id
#captcha_solution=raw_input('输入验证码:')
#post_data = {"source":"radio",'alias': alias, 'form_password':form_password,'captcha_solution':captcha_solution,"captcha_id":captcha_id}

url_fav_song = 'http://douban.fm/mine?type=liked&start='
url_song_info = 'http://38bef685.dotcloud.com/song/'
url_play_list = 'http://douban.fm/j/mine/playlist?type=n&h=&channel=0&from=mainsite&r=4941e23d79'

start = 0
reg_sid = re.compile('sid="(\d+)"')
fail_retry = 2
fail_downloads = []
success_downloads = []
songs=''

class DoubanView(MethodView):
	captcha_id=''
	def  get(self):
		captcha_id=opener.open(url_pic_request).read().replace('"','')
		img="http://douban.fm/misc/captcha?size=m&id=%s" % captcha_id
		return render_template('douban_login.html',img=img,cap_id=captcha_id)
	def post(self):
		alias = request.form['alias']
		form_password = request.form['pwd']
 		captcha_id=request.form['cap_id']
		captcha_solution=request.form['cap']
		post_data = {"source":"radio",'alias': alias, 'form_password':form_password,'captcha_solution':captcha_solution,"captcha_id":captcha_id}
		print post_data
		lg = opener.open(url_login, urllib.urlencode(post_data)).read()

		if lg.find('user_info') < 0:
			print u'登录失败:'
			print lg
	 	songs=down_load_songs(0)
		return songs

def down_load_songs(_start, sids=None):
    global fail_downloads, fail_retry, start
    songs=''

    if not sids:
        fav_page = opener.open(url_fav_song + str(_start)).read()
        sids = reg_sid.findall(fav_page)

    for sid in sids:
        print '---===---'
        print 'down load song sid =', sid

        try:
           songs+= down_load_song(sid)
        except Exception,e:
            fail_downloads.append(sid)
            print 'down load error:', e

        print '\r\n-- END --'
        print ''

    if _start is not None and len(sids) > 14:
        start += len(sids)
        return (down_load_songs(start))
    elif fail_retry > 0 and len(fail_downloads) > 0:
        print '--== retry ==--'
        temp = fail_downloads
        fail_downloads = []
        fail_retry -= 1
        return down_load_songs(None, temp)

def down_load_song(sid):
    global fail_downloads, fail_retry, success_downloads, start

    song = opener.open(url_song_info + str(sid)).read()
    try:
        song = json.loads(song)
    except:
        song = None
    if not song:
        print u'load song error, song id is:', song
        fail_downloads.append(sid)
        return

    if not song.has_key('sid') or not song.has_key('ssid'):
        fail_downloads.append(sid)
        print 'song has no "sid" or "ssid" : ', song
        return

    print 'down load : ', song['title']

    start_cookie = '%sg%sg0' % (song['sid'], song['ssid'])
    ck = ck = cookielib.Cookie(version=0, name='start', value=start_cookie, port=None, port_specified=False, domain='.douban.fm', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cj.set_cookie(ck)
    pl = opener.open(url_play_list).read()
    try:
        pl = json.loads(pl)
    except:
        print 'load play list error:', pl
        fail_downloads.append(sid)
        return

    if pl['song'][0]['sid'] != str(sid):
        print 'load song info ERROR: NOT THE SAME SID'
        fail_downloads.append(sid)
        return

    url = pl['song'][0]['url']

    print '==>> wget: ==>> ', url

    return url+','
    success_downloads.append(sid)