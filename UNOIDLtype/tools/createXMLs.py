#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from createXCUs import Elem
from settings import getDIC, createBK
import glob
def createComponentNode(p):  # Python UNO Component Fileの登録。
    nd = Elem("component",{"loader":"com.sun.star.loader.Python","uri":p.f})
    nd.append(Elem("implementation",{"name":p.imple_name}))
    nd[0].append(Elem("service",{"name":p.service_name}))
    print(p.f + " is registered in the .components file.")
    return nd
def createComponentsFile(filename, DIC):  # .componentファイルの作成。
    createBK(filename, DIC["BACKUP"])  # 引数のファイルがあれば拡張子bkを付ける。
    with open(filename,"w",encoding="utf-8") as f:
        rt = Elem("components",{"xmlns":"http://openoffice.org/2010/uno-components"})
        for p in DIC["Pycompos"]:
            rt.append(createComponentNode(p))
        tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(f.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print(filename + " file has been created.")
def addcfgNode(f):
    return Elem("manifest:file-entry",{"manifest:full-path":f,"manifest:media-type":"application/vnd.sun.star.configuration-data"})
def createManifestFile(component_file, DIC):  # manifext.xmlファイルの作成
    mani = os.path.join(DIC["SRC_PATH"],"META-INF","manifest.xml")  # manifest.xmlの絶対パスを取得。
    if not os.path.exists("META-INF"):  # META-INFフォルダがなければ作成する。
        os.mkdir("META-INF")
    else:
        createBK(mani, DIC["BACKUP"])  # 既存のファイルを拡張子bkでバックアップ。  
    with open(mani,"w", encoding="utf-8") as f:
        rt = Elem("manifest:manifest",{"xmlns:manifest":"http://openoffice.org/2001/manifest"})
        xcus = glob.glob("*.xcu")  # xcuファイルのリストを取得。
        addonsxcu = "Addons.xcu"
        if addonsxcu in xcus:  # Addons.xcuファイルがあるときは先頭のノードにする。
            rt.append(addcfgNode(addonsxcu))
            xcus.remove(addonsxcu)  # 追加したAddons.xcuファイルをリストから削除。
        for xcu in xcus:  # 他のxcuファイルを追加。
            rt.append(addcfgNode(xcu))
        unordb_file = DIC["BASENAME"] + ".uno.rdb"  # rdbファイル名の取得。    
        if os.path.exists(unordb_file):
            rt.append(Elem("manifest:file-entry",{"manifest:full-path":unordb_file,"manifest:media-type":"application/vnd.sun.star.uno-typelibrary;type=RDB"}))
        if os.path.exists(component_file):
            rt.append(Elem("manifest:file-entry",{"manifest:full-path":component_file,"manifest:media-type":"application/vnd.sun.star.uno-components"}))
        tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(f.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print("manifest.xml file has been created.")        
def createXMLs(DIC=None):
    if DIC is None:
        DIC = getDIC()
    component_file = DIC["BASENAME"] + ".components"  # .componentsファイル名の作成。
    os.chdir(DIC["SRC_PATH"])  # srcフォルダに移動。  
    createComponentsFile(component_file, DIC)  # .componentファイルの作成。
    createManifestFile(component_file, DIC)  # manifext.xmlファイルの作成
if __name__ == "__main__":
    createXMLs()