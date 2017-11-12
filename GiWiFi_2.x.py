import urllib,urllib2,urlparse,json,sys,time,os

def get_rel_url():
	url='http://172.21.1.1:8062/redirect'
	req = urllib2.Request(url = url)
	res = urllib2.urlopen(req)
	
	return res.geturl()
def qs(url):
    query = urlparse.urlparse(url).query
    rs_json = dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])
    return rs_json

urljson = json.loads(json.dumps(qs(get_rel_url())))

def get_gw_address():
	return urljson['gw_address']

def get_local_mac():
	return urljson['mac']

def get_local_ip():
	return urljson['ip']

def get_gw_mac():
	return urljson['apmac']

def get_gw_port():
	return urljson['gw_port']

def get_gw_ssid():
	return urljson['gw_id']
#账号
login_phone = "xxxxx"
#密码
login_password = "xxxxx"

json_data = {'gw_id':'GWIFI-zhengzhouhenanjidian',
		'gw_address':''+get_gw_address()+'',
		'gw_port':''+get_gw_port()+'',
		'url':'http://www.baidu.com',
		'ip':''+get_local_ip()+'',
		'mac':''+get_local_mac()+'',
		'apinfo':'',
		'btype':'pc',
		'PHPSESSID':'',
		'olduser':'0',
		'page_time':''+str(int(time.time()))+'',
		'lastaccessurl':'',
		'user_agent':'',
		'devicemode':'',
		'access_type':'0',
		'station_sn':'2851320eb741',
		'client_mac':''+get_gw_mac()+'',
		'online_time':'0',
		'logout_reason':'7',
		'contact_phone':'400-038-5858',
		'suggest_phone':'400-038-5858',
		'station_cloud':'login.gwifi.com.cn',
		'acsign':'800ec48e04be9a2ea9804ce64648887e',
		'name':''+login_phone+'',
		'password':''+login_password+'',
		'service_type':'1'
		}
def login():
	
	data= urllib.urlencode(json_data).encode(encoding='UTF-8')
	url = 'http://login.gwifi.com.cn/cmps/admin.php/api/loginaction?round=308'
	req = urllib2.Request(url,data =data)
	res = urllib2.urlopen(req)
	login_json = res.read()
	auth_json = json.loads(login_json)
	auth_url = auth_json['info']
	end_login_status = urllib2.urlopen(urllib2.Request(auth_url))

	return end_login_status

def get_login_status():
	wifi_status_json = urllib2.urlopen(urllib2.Request("http://"+get_gw_address()+":"+get_gw_port()+"/wifidog/get_auth_state?ip="+get_local_ip()))
	status_json = json.loads(wifi_status_json.read())['data']
	auth_status = json.loads(status_json)['auth_state']
	if auth_status == 2:
		status = "GiWiFi online"
	else:
		status = "GiWiFi offline"
	return status


get_json = json.loads(urllib2.urlopen(urllib2.Request("http://"+get_gw_address()+":"+get_gw_port()+"/wifidog/get_auth_state?ip="+get_local_ip())).read())['data']
end_status = json.loads(get_json)['auth_state']
if end_status == 2:
	print 'Login_Status:',get_login_status()
while 1>0:
	get_json = json.loads(urllib2.urlopen(urllib2.Request("http://"+get_gw_address()+":"+get_gw_port()+"/wifidog/get_auth_state?ip="+get_local_ip())).read())['data']
	end_status = json.loads(get_json)['auth_state']
	if end_status != 2:
	    print 'Start login GiWiFi ......'
	    login()
	    print 'Login_Status:',get_login_status()
	time.sleep(1)