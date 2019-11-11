#!/usr/bin/python
# -*- coding: UTF-8 -*-
import readline
import hashlib
from pyDes import *
import json
import base64


class ShaEncry:
    def __init__(self, deskey = None):
        self.deskey = deskey

    def shaencry(self, data):
        if self.deskey is None:
            hsobj = hashlib.sha256()
        else:
            hsobj = hashlib.sha256(self.deskey.encode("utf-8"))
        hsobj.update(data.encode("utf-8"))
        return hsobj.hexdigest()


class DesEncry:
    def __init__(self, deskey, desiv):
        self.deskey = deskey
        self.iv = desiv

    def desencry(self, data):
        # str 明文password
        # key uid
        des_key = (self.deskey  + "0000")[0:8]
        k = des(des_key, CBC, self.iv, pad=None, padmode=PAD_PKCS5)
        encryptstr = k.encrypt(data)
        return base64.b64encode(encryptstr)  # 转base64编码返回

    def desdescry(self, data):
        # str 密文password
        # key uid
        des_key = (self.deskey + "0000")[0:8]
        if len(data) % 3 == 1:
            data += "=="
            print("==")
        elif len(data) % 3 == 2:
            data += "="
            print("=")
        encryptstr = base64.b64decode(data)
        k = des(des_key, CBC, self.iv, pad=None, padmode=PAD_PKCS5)
        decryptstr = k.decrypt(encryptstr)
        return decryptstr


if __name__ == "__main__":
    print("请选择功能：")
    print("1.密码加密")
    print("2.DES解密")
    number = input("请输入序号：")
    if number == "1":
        print("SHA256密码加密")
        sha = ShaEncry()
        userdata = input("输入待加密的字符串：")
        print(sha.shaencry(userdata))
    elif number == "2":
        print("DES解密")
        mydeskey = "Bdsk/5dkERlkPKDdfsl;fDSFindFlsd&d*&sdkwqOlB"
        myiv = "Bdsk/5dkERlkPKDdfsl;fDSFindFlsd&d*&sdkwqOlB"
        des2 = DesEncry("Bdsk/5dk", "ERlkPKDd")
        userdata = input("输入解密的字符串：")
        print("--------")
        print("--------")
        jsondata = json.loads(bytes.decode(des2.desdescry(userdata)))
        encodedjson = json.dumps(jsondata, indent=2, ensure_ascii=False)
        print(encodedjson)

