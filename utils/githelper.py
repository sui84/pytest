try:
    import requests
except Exception,e:
    import requests

token=''
headers={'Authorization': 'token %s' % token}

def ValidateToken():
    user = requests.get('https://api.github.com/user', headers=headers)
    if user.status_code == 200:
        print user.json()
    else:
        print user.status_code,user.reason


def GetPos():
    pos=requests.get('https://api.github.com/user/repos',headers=headers)
    if pos.status_code == 200:
        repos=pos.json()
        urls=[(lambda x:x.get('url'))(x)for x in repos]
        print urls
        return urls
    else:
        print pos.status_code,pos.reason

def DeletePos(urls):
    for url in urls:
        response=requests.delete(url,headers=headers)
        if response.status_code == 200:
            print "deleted ",url
        else:
            print "delete failed ",url

def RenamePos(url,name,desc):
    #url='https://api.github.com/repos/sui84/pytest'
    payload = {'description': desc, 'name': name}
    response = requests.patch(url, json=payload, headers=headers)
    print 'path ',response.status_code

if __name__ == '__main__':
    ValidateToken()
    urls = GetPos()

