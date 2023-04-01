#!/usr/bin/python

# lrdcq
# usage python wxapkg_pack.py filename, pack at filepath pack

import sys
import os
import struct
import json


class WxapkgFile:
    nameLen = 0
    name = ""
    offset = 0
    size = 0


def run(folder):

    # print('root: {}'.format(root))
    # folderPath = os.path.dirname(folder)
    # print('folderPath: {}'.format(folderPath))
    # sf = os.path.split(folder)
    # print('sf: {}'.format(sf))
    indexInfoLength = 4
    bodyInfoLength = 0
    offset = 14
    fileList = os.walk(folder)
    fileCount = 0
    wxapkgFiles = []
    for root, dirs, files in fileList:
        # print('root, dirs, files: {} {} {}'.format(root, dirs, files))
        for file in files:
            fileCount += 1
            abPath = root + "\\" + file
            print('1111file: {}'.format(abPath))
            name = abPath.replace(folder, '')

            data = WxapkgFile()
            data.name = name.replace("\\", "/")
            data.nameLen = len(name)
            data.size = os.path.getsize(abPath)
            data.offset = 0
            indexInfoLength += (12 + data.nameLen)
            bodyInfoLength += data.size

            wxapkgFiles.append(data)
    # wxapkgFiles = sorted(wxapkgFiles, key=lambda o: o.name)
    offset += indexInfoLength

    wxFiles = [
        '/assets/internal/config.e6604.json', '/assets/internal/import/09/0967b326a.1f618.json', '/assets/internal/native/02/0275e94c-56a7-410f-bd1a-fc7483f7d14a.cea68.png', '/assets/start-scene/config.855f2.json', '/assets/start-scene/import/06/061096640.d3cef.json', '/assets/start-scene/native/08/08518b16-715f-42a7-8882-0083786ea957.353d5.png', '/assets/start-scene/native/1e/1e96ff0f7.e6d79.png', '/assets/start-scene/native/40/40962d94-4e79-4582-b35f-28688210343e.6943b.png', '/assets/start-scene/native/d8/d81ec8ad-247c-4e62-aa3c-d35c4193c7af.cdbc9.png', '/cocos/plugin.json', '/cocos/signature.json', '/app-config.json', '/wx-open-data-project/assets/internal/native/02/0275e94c-56a7-410f-bd1a-fc7483f7d14a.cea68.png', '/wx-open-data-project/assets/resources/native/1a/1a5efd2b2.20e6b.png', '/wx-open-data-project/assets/resources/native/6d/6dfc6daa-cb90-4d05-b3d6-f4ef1dcdd2ee.e1a73.png', '/game.js', '/subContext.js'
    ]
    newWxapkgFiles = []
    for wxfile in wxFiles:
        newWxFile = list(filter(lambda w: w.name == wxfile, wxapkgFiles))
        newWxapkgFiles.append(newWxFile[0])

    for wxapkgFile in newWxapkgFiles:
        wxapkgFile.offset = offset
        offset += wxapkgFile.size
        print('File: {} at Offset = {} size ={} nameLen = {}'.format(
            wxapkgFile.name, wxapkgFile.offset, wxapkgFile.size, wxapkgFile.nameLen))
    # print('fileCount: {}'.format(fileCount))
    root = os.getcwd()
    with open(root + "/" + 'weijiami.wxapkg', 'wb') as f:
        f.write(struct.pack('B', 0xBE))
        f.write(struct.pack('>L', 0))
        f.write(struct.pack('>L', indexInfoLength))
        f.write(struct.pack('>L', bodyInfoLength))
        f.write(struct.pack('B', 0xED))
        f.write(struct.pack('>L', fileCount))
        for wxapkgFile in newWxapkgFiles:
            f.write(struct.pack('>L', wxapkgFile.nameLen))
            f.write(bytes(wxapkgFile.name, encoding='utf-8'))
            f.write(struct.pack('>L', wxapkgFile.offset))
            f.write(struct.pack('>L', wxapkgFile.size))
        for wxapkgFile in newWxapkgFiles:
            with open(folder + wxapkgFile.name, 'rb') as fr:
                content = fr.read()
                f.write(content)
                fr.close()
        f.close()


if __name__ == '__main__':
    # fname = 'wx7c8d593b2c3a7703_3.wxapkg'
    folder = r'D:\03_mycode\yangleyang\jiemi.wxapkg.unpack'
    run(folder)
