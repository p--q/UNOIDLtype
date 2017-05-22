#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import glob
import os
import sys
src_path = os.path.join(os.path.dirname(sys.path[0]), "src")  # srcフォルダの絶対パスを取得。





# This name will be rdb file name, .components file name, oxt file name.
# BASE_NAME = "PyUnoComponent"  # これがrdbファイル名、.componentsファイル名、oxtファイル名になる。
# 
# # a list of a dict of Python UNO Component Files: (file name,service implementation name, service name,handled protocol)
# LST = [{
#     "PYTHON_UNO_Component": BASE_NAME + ".py",  # Python UNO Componentファイル名。これからのimportはunoのモジュールが読み込めないエラーが出るから無理。
#     "IMPLE_NAME":'UnoInsp',  # 実装サービス名
#     "SERVICE_NAME":'com.blogspot.pq.UnoInsp',  # サービス名
#     "HANDLED_PROTOCOL":""  # プロトコール名
#     }] 


def createBK(path):  # 引数のファイルがあれば拡張子bkを付ける。
    if os.path.exists(path):  #ファイルがすでに存在するとき。
        bk = path + ".bk"  # バックアップファイル名の取得。
        if os.path.exists(bk): os.remove(bk)  # Windowsの場合は上書きできないので削除が必要。
#         os.rename(path, bk)  # 既存のファイルを拡張子bkでバックアップ。 
#         print("The previous version of " + os.path.basename(path) + " file has been renamed for backup.")  
def main():
    imp = "IMPLE_NAME"
    ser = "SERVICE_NAME"       
    os.chdir(src_path)  # srcフォルダに移動。
    pys = glob.glob("*.py")  # srcフォルダのpyファイルを取得。
    if pys:
        pycompo = pys[0]
        BASE_NAME, _ = os.path.splitext(pycompo)
        LST = [{
            "PYTHON_UNO_Component": pycompo,  # Python UNO Componentファイル名。これからのimportはunoのモジュールが読み込めないエラーが出るから無理。
            imp: None,  # 実装サービス名
            ser: None,  # サービス名
            "HANDLED_PROTOCOL": None  # プロトコール名
            }] 
        with open(pycompo, "r") as f:
            d = dict()
            for line in f:
                if line.startswith(imp):
                    exec(line, d)
                    LST[0][imp] =  d[imp]
                elif line.startswith(ser):
                    exec(line, d)
                    LST[0][ser] =  d[ser]
                elif LST[0][imp] and LST[0][ser]:
                    break
if __name__ == "__main__":
    sys.exit(main())