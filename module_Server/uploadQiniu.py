
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qiniu
import urllib
import sys
import os
import msvcrt
import datetime
import subprocess

__author__ = "lizhe"


"""将图片拖曳到此脚本即可自动上传

会在同文件目录下生成图片的markdown格式引用地址
使用前先配置好下面的参数
"""

# ----------------手动配置区---------------
accessKey = 'wpirGksfiaI_lpv8IuPhOfc5sQ0Fk1v78jePJlfA'
secretkey = 'tb1zs872KEMINV3zd0A8RzEtsdG8jnVypAcWdKxq'
# 上传空间的域名，需要自己去后台获取
bucket_url = {
    'woshichuanqilz': 'http://7xpvdr.com1.z0.glb.clouddn.com/',
}
bucket = 'woshichuanqilz'  # 上传空间

# ----------------默认配置区-------------------------
img_suffix = ["jpg", "jpeg", "png", "bmp", "gif"]
os.chdir(sys.path[0])
result_file = "PicUrl.txt"  # 保存上传结果

class Qiniu(object):

    """七牛上传与下载的工具类

    需要七牛的Python SDK
    pip install qiniu
    SDK详细用法见　http://developer.qiniu.com/docs/v6/sdk/python-sdk.html
    """
    SUCCESS_INFO = "上传成功！"

    def __init__(self, accessKey, secretkey):
        self.accessKey = accessKey
        self.secretkey = secretkey
        self._q = qiniu.Auth(self.accessKey, self.secretkey)

    def upload_file(self, bucket, up_filename, file_path):
        """上传文件

        Args:
            bucket: 上传空间的名字
            up_filename: 上传后的文件名
            file_path:   本地文件的路径
        Returns:
            ret:     dict变量，保存了hash与key（上传后的文件名）
            info:    ResponseInfo对象，保存了上传信息
            url:     st, 上传后的网址
        """
        token = self._q.upload_token(bucket)
        ret, info = qiniu.put_file(token, up_filename, file_path)
        url = self.get_file_url(bucket, up_filename)
        return ret, info, url

    def get_file_url(self, bucket, up_filename):
        if not bucket in bucket_url.keys():
            raise AttributeError("空间名不正确！")
        url_prefix = bucket_url[bucket]
        url = url_prefix + urllib.parse.quote(up_filename)
        return url

def save(filename, url):
    line = "[%s](%s)\n" % (filename, url)
    # 如果是图片则生成图片的markdown格式引用
    if os.path.splitext(filename)[1][1:] in img_suffix:
        line = "!" + line
    with open(result_file, "a", encoding="utf-8") as f:
        f.write(line)

def getTimeStr():
    """返回 2015/11/18/17/16/8/ 形式的字符串
    如果上传同名文件且前缀相同，则后上传的文件会顶掉先前的
    加时间作为前缀，即便于检索，又避免此问题
    """
    now = datetime.datetime.now()
    tmp = tuple(now.timetuple())[:-3]
    tmp = map(str, tmp)
    return "/".join(tmp) + "/"

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def UploadQNFile(uploadfile):
    print('in uplaod')
    q = Qiniu(accessKey, secretkey)
    timeStr = getTimeStr()

    if os.path.isfile(uploadfile):
        suffix = os.path.splitext(uploadfile)[1][1:]
        name = os.path.split(uploadfile)[1]
        ret, info, url = q.upload_file(bucket, name, uploadfile)
        print("Uploaded :  %s " % name)
        save(name, url)
    else:
        print('file doesn\'t exist')
    up_filename=bucket_url['woshichuanqilz'] + name
    if os.path.splitext(name)[1][1:] in img_suffix:
        fileLink='![' + name + '](' + up_filename + ')'
    print('out upload')
    return up_filename
