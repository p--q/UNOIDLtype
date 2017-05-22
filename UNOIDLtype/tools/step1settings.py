#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import glob
import os
import sys
SRC_PATH = os.path.join(os.path.dirname(sys.path[0]), "src")  # srcフォルダの絶対パスを取得。
def createBK(path):  # 引数のファイルがあれば拡張子bkを付ける。
    if os.path.exists(path):  #ファイルがすでに存在するとき。
        bk = path + ".bk"  # バックアップファイル名の取得。
        if os.path.exists(bk): os.remove(bk)  # Windowsの場合は上書きできないので削除が必要。
        os.rename(path, bk)  # 既存のファイルを拡張子bkでバックアップ。 
        print("The previous version of " + os.path.basename(path) + " file has been renamed for backup.")  
def main():
    imp = "IMPLE_NAME"  # 実装サービス名の辞書のキー。
    ser = "SERVICE_NAME" # サービス名の辞書のキー。
    os.chdir(SRC_PATH)  # srcフォルダに移動。
    pys = glob.glob("*.py")  # srcフォルダの直下にあるpyファイルのリストを取得。複数ファイルには未対応。
    if pys:  # pyファイルが取得できた時
        pycompo = pys[0]  # pyファイル名を取得。
        BASE_NAME, _ = os.path.splitext(pycompo)  # pyファイルの拡張子以外の名前を取得。  # これがrdbファイル名、.componentsファイル名、oxtファイル名になる。
        DIC = {
            "ComponentFile": pycompo,  # Python UNO Componentファイル名。
            imp: None,  # 実装サービス名
            ser: None,  # サービス名
            "HANDLED_PROTOCOL": None  # プロトコールハンドラー名。未対応。
            }
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
if __name__ == "__main__":
    sys.exit(main())
    
    
    
