#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from settings import getDIC, createBK
import os
import glob

def createIDL(DIC=None):
    if DIC is None:
        DIC = getDIC()
        
    com.blogspot.pq.UnoInsp
    XUnoInsp.idl
    
    
        
        
    myidl_path = os.path.join(DIC["SRC_PATH"],"idl")  # PyDevプロジェクトのidlフォルダへの絶対パスを取得。
    if not os.path.exists(myidl_path):  # idlフォルダがないとき
        os.mkdir(myidl_path)  # idlフォルダを作成。
    os.chdir(myidl_path)  # idlフォルダに移動
    for i in glob.iglob("*.idl"):  # すでにあるidlファイルを削除。
        createBK(i, DIC["BACKUP"]) 
        
        
 
        
if __name__ == "__main__":
    createIDL()        