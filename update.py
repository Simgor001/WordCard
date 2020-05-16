import requests
import urllib3
import sys
import os
import tempfile
from contextlib import closing


def temp_file(suffix=''):
    return tempfile.mktemp(dir=os.environ['temp'], suffix=suffix)


def update(verstion):
    print('正在获取更新...')
    try:
        ver = requests.get('http://wordcard.eace.top/Version').text

        print('最新版本：%s,当前版本：%s' % (ver, verstion))
        if int(verstion.replace('.', '')) >= int(ver.replace('.', '')):
            return
        print('正在更新...')
        urllib3.disable_warnings()
        url = 'http://wordcard.eace.top/update/update_%s.exe'%ver
        with closing(requests.get(url, verify=False, stream=True)) as res:
            res.raise_for_status()
            update_file = temp_file('.exe')
            for chunk in res.iter_content(chunk_size=10240000000):
                with open(update_file, 'wb') as f:
                    if chunk:
                        f.write(chunk)
        print('正在安装更新...')
        os.system('start %s' % update_file)
    except:
        print('更新失败！')
