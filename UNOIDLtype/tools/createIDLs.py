#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from settings import getDIC, createBK
import os
import glob
def defineIDLs():  # IDLの定義を設定する。継承しているUNOIDLのidlファイルは自動include。
    # com.blogspot.pq.UnoInspの定義
    unoinsp = UNOIDL("com.blogspot.pq.UnoInsp")
    unoinsp.setSuper("XUnoInsp")
    yield unoinsp
    # com.blogspot.pq.XUnoInspの定義
    xunoinsp = UNOIDL("com.blogspot.pq.XUnoInsp")
    xunoinsp.setSubs(
        "string stringTypeArg([in] string value)",
        "sequence <string> stringSeqenceTypeArg([in] sequence <string> values)",
        "boolean booleanTypeArg([in] boolean boo)",
        "any anyTypeArg([in] any obj)",
        "sequence <any> getInitArgs()"
        )
    yield xunoinsp
class UNOIDL:
    def __init__(self, name):  # UNOIDLのフルネームを引数にする。
        self.name = name
        self.includes = tuple()
        self.subs = tuple() 
        self.super = ""
    def setIncludes(self, *args):  # includeするidlファイルを取得。
        self._args(args, "includes")
    def setSubs(self, *args):  # 定義したUNOIDLがもつものを取得。com.sun.star.uno.XInterfaceは自動追加。 
        self._args(args, "subs")     
    def setSuper(self, super):  # 定義したUNOIDLが継承するものを取得。
        self.super = super
    def _args(self, args, attr):
        if len(args) > 0:
            setattr(self, attr, args)  
    def getVal(self):  #
        tab = "    "  # インデント
        name_underscore = "_" + self.name.replace(".", "_") + "_idl_"
        ms = self.name.split(".")  # UNOIDLのパスを分割。
        name_base = ms.pop()  # パスのないUNOIDL名を取得。
        interface = name_base.startswith("X")  # インターフェイスであればTrue
        ms = list(map(lambda x: "module " + x, ms))
        s = "interface " if interface else "service "
        ms.append("\n" + tab + s + name_base)
        if self.subs:
            s = self._superInclude(ms.pop(), interface)
            ms.append(s + " {\n" + ";\n".join(map(lambda x:tab * 2 + x, self.subs)) + ";\n" + tab + "};\n")               
        else:
            s = self._superInclude("", interface)
            ms[-1] += s + ";\n"    
        return name_underscore, self._createNested(ms), name_base + ".idl"  
    def _superInclude(self, s, interface):
        xinterface = "com.sun.star.uno.XInterface"
        if interface:  # インターフェイスのとき
            if not self.super.rsplit(".")[-1].startswith("X"):  # インターフェイスを継承していなければXInterfaceを継承する。
                self.setSuper(xinterface)
        if self.super:  # 継承している時
            if not self.super in self.includes:  # 継承したIDLをinculudeしてなければ
                self.includes = list(self.includes)
                self.includes.append(self.super)  # includeに追加。
            if not self.super == xinterface:  # XInterfaceは表記しない。
                s += " : " + self.super.replace(".", "::")
        return s
    def _createNested(self, ms):
        s = ""
        ms.reverse()
        out = ms.pop()
        for m in ms:
            s = " {" + m + s + "};"
        s = out + s
        return s
def createIDL(DIC=None):
    if DIC is None:
        DIC = getDIC()
    myidl_path = os.path.join(DIC["SRC_PATH"],"idl")  # PyDevプロジェクトのidlフォルダへの絶対パスを取得。
    if not os.path.exists(myidl_path):  # idlフォルダがないとき
        os.mkdir(myidl_path)  # idlフォルダを作成
    os.chdir(myidl_path)  # idlフォルダに移動     
    for f in glob.iglob("*.idl"):
        createBK(f, DIC["BACKUP"])  # 既存のidlファイルを削除。
    for idl in defineIDLs():
        name_underscore, m, fn = idl.getVal()
        with open(fn, "w", encoding="utf-8") as f:
            lines = list()
            lines.append("#ifndef " + name_underscore)
            lines.append("#define " + name_underscore)
            lines.append("")
            for inc in idl.includes:
                s = inc.replace(".", "/") + ".idl"
                lines.append("#include <" + s + ">")  
            lines.extend(["", m, "", "#endif"])
            f.write("\n".join(lines))
            print(fn + " has been created.")
if __name__ == "__main__":
    createIDL()        