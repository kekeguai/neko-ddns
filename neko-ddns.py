import requests
import json
from dns import resolver

def checkDomain(domain: str):
    res = resolver.Resolver()
    res.nameservers = ['1.1.1.1']
    answers = res.resolve(domain)
    for rdata in answers:
        return(rdata.address)


def get_neko_ip(name, token: str):
    url = 'https://relay.nekoneko.cloud/api/servers'
    payload = {}
    headers = {
        "content-type": "application/json",
        "token": token
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    json_string = json.loads(r.content.decode())
    if json_string['status'] == 1:
        for sublist in json_string['data']:
            if sublist['name'] == name:
                return(sublist['host'])
        raise ValueError("節點不存在")

def cf_getid(cf_auth_email, cf_auth_key, cf_auth_method, cf_zone_identifier, cf_record_name):
    url = "https://api.cloudflare.com/client/v4/zones/" + cf_zone_identifier +"/dns_records?type=A&name=" + cf_record_name
    payload = {}
    headers = {
        "X-Auth-Email": cf_auth_email,
        "Authorization": "Bearer " + cf_auth_key,
        # Set auth_header to "X-Auth-Key:" if using global api
        "content-type": "application/json",
    }
    r = requests.get(url, data=json.dumps(payload), headers=headers)
    json_string = json.loads(r.content.decode())
    record_identifier = json_string.get('result')[0].get('id')
    print("記錄ID爲: " + record_identifier)
    return record_identifier

def cf_ip_update(cf_auth_email, cf_auth_key, cf_auth_method, cf_zone_identifier, cf_record_name, record_identifier, new: str):
    url = "https://api.cloudflare.com/client/v4/zones/" + cf_zone_identifier +"/dns_records/" + record_identifier
    payload = {
        "type": "A",
        "name": cf_record_name,
        "content": new,
        "ttl": 1,
        "proxied": False
    }
    headers = {
        "X-Auth-Email": cf_auth_email,
        "Authorization": "Bearer " + cf_auth_key,
        # Set auth_header to "X-Auth-Key:" if using global api
        "content-type": "application/json",
    }
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    json_string = json.loads(r.content.decode())
    print ("更新完成")

def main():
    token = "<YOUR NEKO API TOKEN HERE>" 
    name  = "<需要檢測的線路名字>"
    
    cf_auth_email = "" # The email used to login 'https://dash.cloudflare.com'
    cf_auth_key = "" # Your API Token or Global API Key
    cf_auth_method = "token" # Set to "global" for Global API Key or "token" for Scoped API Token
    cf_zone_identifier = "" # Can be found in the "Overview" tab of your domain
    cf_record_name = "" # Which record you want to be synced
    
    
    neko_ip = get_neko_ip(name, token)
    cf_ip = checkDomain(cf_record_name)
    print("API 獲得的IP爲: " + neko_ip)
    print("CF 解析的IP爲: " + cf_ip)
    
    if (cf_ip != neko_ip):
        print("IP地址有變動，執行更新")
        record_identifier = cf_getid(cf_auth_email, cf_auth_key, cf_auth_method, cf_zone_identifier, cf_record_name)
        cf_ip_update(cf_auth_email, cf_auth_key, cf_auth_method, cf_zone_identifier, cf_record_name, record_identifier, neko_ip)
    else:
        print("IP一致，無需更新IP")
    
if __name__ == "__main__":
    main()
