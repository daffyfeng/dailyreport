#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1
from Crypto.Cipher import AES
import struct


# 微信小程序包 自定义标识
WXAPKG_FLAG = 'V1MMWX'
WXAPKG_FLAG_LEN = len(WXAPKG_FLAG)


def main():

    parser = argparse.ArgumentParser(description='PC微信小程序wxapkg包加密工具')
    parser.add_argument('--wxid', metavar='微信小程序ID', required=True)
    parser.add_argument('--iv', metavar='iv', required=False,
                        default='the iv: 16 bytes')
    parser.add_argument('--salt', metavar='salt',
                        required=False, default='saltiest')
    parser.add_argument('-f', '--file', metavar='待加密的小程序包文件路径', required=True)
    parser.add_argument(
        '-o', '--output', metavar='加密后的小程序包文件路径', required=True)

    args = parser.parse_args()

    key = PBKDF2(args.wxid.encode('utf-8'), args.salt.encode('utf-8'),
                 32, count=1000, hmac_hash_module=SHA1)

    # 读取加密的内容
    if not os.path.exists(args.file):
        raise Exception('文件不存在')

    with open(args.file, mode='rb') as f:
        dataByte = f.read()

    # 初始化密钥
    cipher = AES.new(key, AES.MODE_CBC, args.iv.encode('utf-8'))
    # dataStr = dataByte[0: 1023].decode('utf-8')
    # dataStr += ' '
    dByte = bytearray()
    for i in range(1023):
        dByte.append(dataByte[i])
    dByte.append(bytes(b'\x01')[0])

    # 加密头部1023个字节
    originData = cipher.encrypt(
        dByte)

    # 初始化xor密钥, 解密剩余字节
    xorKey = 0x66
    if len(args.wxid) >= 2:
        xorKey = ord(args.wxid[len(args.wxid) - 2])

    afData = dataByte[1023:]

    out = bytearray()
    for i in range(len(afData)):
        out.append(afData[i] ^ xorKey)

    originData = originData[0:1024]

    # 保存加密后的数据
    with open(args.output, mode='wb') as f:
        f.write(WXAPKG_FLAG.encode('utf-8'))
        f.write(originData)
        f.write(out)

    print('加密成功', args.output)


if __name__ == "__main__":
    main()
