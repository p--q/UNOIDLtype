#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from step3createXCUs import Elem
from step1settings import BASE_NAME,LST,createBK,src_path
import glob
def createComponentNode(dic):  # Python UNO Component Fileの登録。
    nd = Elem("component",{"loader":"com.sun.star.loader.Python","uri":dic["PYTHON_UNO_Component"]})
    nd.append(Elem("implementation",{"name":dic["IMPLE_NAME"]}))
    nd[0].append(Elem("service",{"name":dic["SERVICE_NAME"]}))
    print(dic["PYTHON_UNO_Component"] + " is registered in the .components file.")
    return nd
def createComponentsFile(filename):  # .componentファイルの作成。
    createBK(filename)  # 引数のファイルがあれば拡張子bkを付ける。
    with open(filename,"w",encoding="utf-8") as fp:
        rt = Elem("components",{"xmlns":"http://openoffice.org/2010/uno-components"})
        for dic in LST:  # Python UNO Component Fileの登録。
            rt.append(createComponentNode(dic))
        tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print(filename + " file has been created.")
def addcfgNode(f):
    return Elem("manifest:file-entry",{"manifest:full-path":f,"manifest:media-type":"application/vnd.sun.star.configuration-data"})
def createManifestFile(component_file,unordb_file):  # manifext.xmlファイルの作成
    mani = os.path.join(src_path,"META-INF","manifest.xml")  # manifest.xmlの絶対パスを取得。
    if not os.path.exists("META-INF"):  # META-INFフォルダがなければ作成する。
        os.mkdir("META-INF")
    else:
        createBK(mani)  # 既存のファイルを拡張子bkでバックアップ。  
    with open(mani,"w",encoding="utf-8") as fp:
        rt = Elem("manifest:manifest",{"xmlns:manifest":"http://openoffice.org/2001/manifest"})
        xcus = glob.glob("*.xcu")  # xcuファイルのリストを取得。
        addonsxcu = "Addons.xcu"
        if addonsxcu in xcus:  # "Addons.xcu"ファイルがあるときは先頭のノードにする。
            rt.append(addcfgNode(addonsxcu))
            xcus.remove(addonsxcu)
        for xcu in xcus:
            rt.append(addcfgNode(xcu))
        if os.path.exists(unordb_file):
            rt.append(Elem("manifest:file-entry",{"manifest:full-path":unordb_file,"manifest:media-type":"application/vnd.sun.star.uno-typelibrary;type=RDB"}))
        if os.path.exists(component_file):
            rt.append(Elem("manifest:file-entry",{"manifest:full-path":component_file,"manifest:media-type":"application/vnd.sun.star.uno-components"}))
        tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print("manifest.xml file has been created.")        
def main():
    component_file = BASE_NAME + ".components"  # .componentsファイル名の作成。
    unordb_file = BASE_NAME + ".uno.rdb"  # rdbファイル名の取得。
    os.chdir(src_path)  # srcフォルダに移動。  
    createComponentsFile(component_file)  # .componentファイルの作成。
    createManifestFile(component_file,unordb_file)  # manifext.xmlファイルの作成
if __name__ == "__main__":
    sys.exit(main())    