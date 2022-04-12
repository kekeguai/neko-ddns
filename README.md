一鍵更新neko relay域名

因爲neko的国内域名全部被DNS污染，现只提供IP，可以使用本項目配合cron檢測域名是否指向最新IP並更新最新的IP

# 使用方法（多域名）
1. 安装依赖

`pip3 install requets dnspython`

2. 编辑`neko-ddns-multi.py`, 按格式將需要更新的域名寫入名爲`domains`的dictionary中,其餘与单域名一致

# 使用方法 (单域名)
1. 安裝依賴

`pip3 install requests dnspython`

2. 編輯`neko-ddns.py`:
```
res.nameservers = ['1.1.1.1']
```
指定DNS Resolver, 默認值爲`1.1.1.1`

```
token = "<YOUR NEKO API TOKEN HERE>" 
name  = "<需要檢測的線路名字>如<广港链路A>"
```
前往[https://relay.nekoneko.cloud/user/setting](https://relay.nekoneko.cloud/user/setting)獲取API密鑰

```
cf_auth_email = "" # The email used to login 'https://dash.cloudflare.com'
cf_auth_key = "" # Your API Token or Global API Key 
```
前往 [Cloudfalre - Profile - API Tokens](https://dash.cloudflare.com/profile/api-tokens)使用Edit zone DNS模板並在Zone Resources指定你的域名的zone (出於安全考慮，請不要使用global api)

```
cf_auth_method = "token" # Set to "global" for Global API Key or "token" for Scoped API Token
cf_zone_identifier = "" # Can be found in the "Overview" tab of your domain, 在域名的「Overview」頁面中找到域名的Zone ID
cf_record_name = "" # Which record you want to be synced
```

3. 定時執行

使用`crontab -e`添加新規則即可, 请自行替换python路径
`30 * * * * /usr/bin/python3 /path/to/neko-ddns.py`
