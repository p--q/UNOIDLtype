#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import glob
import os
import sys
def createBK(path, flag=True):  # 引数のファイルがあれば拡張子bkを付けてバックアップにする。
    if os.path.exists(path):  #ファイルがすでに存在するとき。
        if flag:
            bk = path + ".bk"  # バックアップファイル名の取得。
            if os.path.exists(bk): 
                os.remove(bk)  # 既存のbkファイルを削除。
            os.rename(path, bk)  # 既存のファイルを拡張子bkでバックアップ。 
            print("The previous version of " + os.path.basename(path) + " file has been renamed for backup.")  
        else:
            os.remove(path)  # 既存のファイルを削除。
class Pycompo:
    def __init__(self, pycompo):  # これがrdbファイル名、.componentsファイル名、oxtファイル名になる。
        self.f = pycompo
        self.imple_name = None
        self.service_name = None
        self.handled_protocol = None
        self.getVal(pycompo)
    def getVal(self, pycompo):  
        imp = "IMPLE_NAME"  # 実装サービス名の辞書のキー。
        ser = "SERVICE_NAME" # サービス名の辞書のキー。     
        with open(pycompo, "r") as f:  # pythonpathフォルダにはまだパスが通らずインポートではエラーが出るのでテキストファイルとして読み込む。
            d = dict()  # exec()の名前空間を受ける辞書。
            for line in f:  # ファイルの先頭の行から読みこむ
                if line.startswith(imp):  # 行頭がimpで始まっている時
                    exec(line, d)  # dにimpを受け取る。
                    self.imple_name = d[imp]  # 実装サービス名を取得。
                elif line.startswith(ser):  # 行頭がserで始まっている時
                    exec(line, d)  # dにserを受け取る。
                    self.service_name = d[ser]  # サービス名を取得。
                elif self.imple_name and self.service_name:  # impとserを取得したらfor文を出る。
                    break
def getDIC():
    print("This script uses the name of the PyDev Project name as the name of the oxt file.")
    DIC = dict()
    DIC["BACKUP"] = True  # ファイルのバックアップ。Falseでしない。
    DIC["Pycompos"] = list()
    DIC["SRC_PATH"] = os.path.join(os.path.dirname(sys.path[0]), "src")  # srcフォルダの絶対パスを取得。
    DIC["BASENAME"] = os.path.basename(os.path.dirname(DIC["SRC_PATH"]))
    os.chdir(DIC["SRC_PATH"])  # srcフォルダに移動。
    for pycompo in glob.iglob("*.py"):  # srcフォルダの直下にあるpyファイルのリストを取得。
        p = Pycompo(pycompo) 
        if p.imple_name and p.service_name:  # 実装サービス名とサービス名を取得できたファイルをPython UNO Componentファイルとみなす。
            DIC["Pycompos"].append(p)
    if not DIC["Pycompos"]:
        print("There is no component file in the src folder.")
        sys.exit()
    return DIC
if __name__ == "__main__":
    DIC = getDIC()
    print(DIC)
  
    
    
    
