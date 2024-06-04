import requests
import json
import re

# Initialize a session object
s = requests.Session()

def loginPage():
    url = "https://member.lazada.co.th/user/login"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://member.lazada.co.th',
        'referer': 'https://member.lazada.co.th/user/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    req = s.get(url, headers=headers)
    pat = re.compile(r'id="X-CSRF-TOKEN" content="(.*?)"')
    res = re.findall(pat, req.text)
    
    if res:
        return {'token': res[0], 'cookie': req.cookies}
    else:
        raise Exception("CSRF token not found")

def login(token):
    url = "https://member.lazada.co.th/user/api/login"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://member.lazada.co.th',
        'referer': 'https://member.lazada.co.th/user/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-csrf-token': token['token']
    }

    data = {'loginName': 'toriqahmads@gmail.com', 'password': 'Kbps1234'}
    
    req = s.post(url, data=json.dumps(data), headers=headers, cookies=token['cookie'])
    reqs = req.json()
    
    if reqs.get('success'):
        return {'cookie': req.cookies, 'content': reqs}
    else:
        raise Exception("Login failed")

def visitProd(token):
    url = "https://www.lazada.co.th/-i174951351-s207287470.html?spm=a2o4j.order_details.details_title..3b896664srxzbW&urlFlag=true&mp=1"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://member.lazada.co.th',
        'referer': 'https://member.lazada.co.th/user/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    req = s.get(url, headers=headers, cookies=token['cookie'])
    pat = re.compile(r'id="X-CSRF-TOKEN" content="(.*?)"')
    res = re.findall(pat, req.text)
    
    if res:
        return {'token': res[0], 'cookie': req.cookies}
    else:
        raise Exception("CSRF token not found on product page")

def addCart(token):
    url = "https://cart.lazada.co.th/cart/api/add"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://member.lazada.co.th',
        'referer': 'https://member.lazada.co.th/user/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-csrf-token': token['token']
    }

    data = [{'itemId': '174951351', 'skuId': '207287470', 'quantity': 1}]
    
    req = s.post(url, data=json.dumps(data), headers=headers, cookies=token['cookie'])
    res = req.json()
    
    if res.get('success'):
        return res
    else:
        raise Exception("Failed to add item to cart")

# Execution
try:
    r = loginPage()
    r2 = login(r)
    r3 = visitProd(r2)
    result = addCart(r3)
    print("Item added to cart successfully:", result)
except Exception as e:
    print("An error occurred:", str(e))
