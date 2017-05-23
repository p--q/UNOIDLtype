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
def getDIC():
    print("This script uses the name of the py file in the src folder as the name of the oxt file.")
    imp = "IMPLE_NAME"  # 実装サービス名の辞書のキー。
    ser = "SERVICE_NAME" # サービス名の辞書のキー。
    src_path = os.path.join(os.path.dirname(sys.path[0]), "src")  # srcフォルダの絶対パスを取得。
    os.chdir(src_path)  # srcフォルダに移動。
    pys = glob.glob("*.py")  # srcフォルダの直下にあるpyファイルのリストを取得。複数ファイルには未対応。
    if pys:  # pyファイルが取得できた時
        pycompo = pys[0]  # pyファイル名を取得。
        DIC = {
            "ComponentFile": pycompo,  # Python UNO Componentファイル名。
            imp: None,  # 実装サービス名
            ser: None,  # サービス名
            "HANDLED_PROTOCOL": None  # プロトコールハンドラー名。自動取得未対応。
            }
        DIC["BASE_NAME"], _ = os.path.splitext(pycompo)  # pyファイルの拡張子以外の名前を取得。  # これがrdbファイル名、.componentsファイル名、oxtファイル名になる。
        DIC["SRC_PATH"] = src_path  # srcフォルダのパス
        DIC["BACKUP"] = False  # ファイルのバックアップ。Falseでしない。
        with open(pycompo, "r") as f:  # pythonpathフォルダにはまだパスが通らずインポートではエラーが出るのでテキストファイルとして読み込む。
            d = dict()  # exec()の名前空間を受ける辞書。
            for line in f:  # ファイルの先頭の行から読みこむ
                if line.startswith(imp):  # 行頭がimpで始まっている時
                    exec(line, d)  # dにimpを受け取る。
                    DIC[imp] = d[imp]  # DICにimpを受け取る。
                elif line.startswith(ser):  # 行頭がserで始まっている時
                    exec(line, d)  # dにimpを受け取る。
                    DIC[ser] = d[ser]  # DICにserを受け取る。
                elif DIC[imp] and DIC[ser]:  # impとserを取得したらfor文を出る。
                    break
            else:
                print("The implementation service name or service name could not be obtained.")     
    else:
        print("There is no component file in the src folder.")
        sys.exit()
    return DIC
if __name__ == "__main__":
    DIC = getDIC()
    print(DIC)
  
    
    
    
