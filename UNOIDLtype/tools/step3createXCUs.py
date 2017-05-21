#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys
from step1settings import LST,createBK,src_path
import types
class Elem(ET.Element):  
    '''
    キーワード引数textでテキストノードを付加するxml.etree.ElementTree.Element派生クラス。
    '''
    def __init__(self, tag, attrib={},**kwargs):  
        if "text" in kwargs:
            txt = kwargs["text"]
            del kwargs["text"]  
            super().__init__(tag,attrib,**kwargs)
            self._text(txt)
        else:
            super().__init__(tag,attrib,**kwargs)
    def _text(self,txt):
        self.text = txt
class MenuItem(Elem):
    '''
    oor:node-type="MenuItem"を作成するメソッドをもつElemの派生クラス。
    '''
    def createNodes(self,dic,xdic):
        '''
        oor:node-type="MenuItem"のElementのリストを返す。
        
        :param dic: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type dic: dict
        :param xdic: Xml Attributes
        :type xdic: dict
        :returns: a list of nodes
        :rtype: list
        '''
        ORDER = "URL","Title","Target","Context","Submenu","ControlType","Width"  # ノードの順を指定。 "ImageIdentifier"ノードは使わないので無視する。
        lst_nd = list()  # ノードをいれるリスト。
        for key in ORDER:
            if key in xdic:
                val = xdic[key]
                if key == "Title":  # タイトルノードのとき
                    nd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                    for lang,txt in val.items():
                        nd.append(Elem("value",{"xml:lang":lang},text=txt))
                    lst_nd.append(nd)
                elif key == "Submenu":  # サブメニューノードのとき
                    fn = val.pop()  # サブメニュー設定のための関数を取得。
                    if type(fn) is types.MethodType:
                        lst_nd.append(fn(dic,val))
                else:  # それ以外のノードの時。
                    nd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                    nd.append(Elem("value",text=val)) 
                    lst_nd.append(nd) 
        return lst_nd 
    def createWindowStateNodes(self,dic,xdic):  # ツールバーの設定。
        '''
        Properties for ToolBar
        
        :param dic: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type dic: dict
        :param xdic: Xml Attributes
        :type xdic: dict
        :returns: a list of nodes
        :rtype: list
        '''
        ORDER = "UIName","ContextSensitive","Visible","Docked" # ノードの順を指定。
        lst_nd = list()  # ノードをいれるリスト。
        for key in ORDER:
            if key in xdic:
                val = xdic[key]
                if key == "UIName":  # タイトルノードのとき
                    nd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                    for lang,txt in val.items():
                        nd.append(Elem("value",{"xml:lang":lang},text=txt))
                    lst_nd.append(nd)
                else:  # それ以外のノードの時。
                    nd = Elem("prop",{"oor:name":key,"oor:type":"xs:boolean"})
                    nd.append(Elem("value",text=val)) 
                    lst_nd.append(nd) 
        return lst_nd         
class AddonMenu(MenuItem):  # ツール→アドオン、に表示されるメニュー項目を作成。
    '''
    Tools->Add-Ons->AddonMenu
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"AddonMenu"})  # 変更不可。
        self.append(Elem("node",{'oor:name':dic["HANDLED_PROTOCOL"] + ".function","oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。
        self[0].extend(super().createNodes(dic,{"Title":{"en-US":"Add-On example by AddonMenuNode"},"Context":"com.sun.star.text.TextDocument","Submenu":["m1","m2",self.subMenu]}))  # ここから表示されるメニューの設定。
    def subMenu(self,dic,val):
        '''
        サブメニューの作成。 
        
        :param dic: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type dic: dict
        :param val: Submenu IDs
        :type val: list
        :returns:  a node for submenu
        :rtype: xml.etree.ElementTree.Element
        
        '''
        nd = Elem("node",{"oor:name":"Submenu"})  # 変更不可。
        i = 0
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function1","Title":{"en-US":"Add-On Function 1"},"Target":"_self"}))
        i += 1
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function2","Title":{"en-US":"Add-On Function 2"},"Target":"_self"}))
        return nd
class OfficeMenuBar(MenuItem):  # メインメニューに追加される項目を作成。
    '''
    OfficeMenuBar
    Main Menu Bar
    
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"OfficeMenuBar"})  # 変更不可。
        self.append(Elem("node",{'oor:name':dic["HANDLED_PROTOCOL"],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。
        self[0].extend(super().createNodes(dic,{"Title":{"en-US":"Add-On example by OfficeMenuBar"},"Target":"_self","Submenu":["m1","m2","m3",self.subMenu]}))  # ここから表示されるメニューの設定。
    def subMenu(self,dic,val):
        nd = Elem("node",{"oor:name":"Submenu"})  # 変更不可。
        i = 0
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function1","Title":{"en-US":"Add-On Function 1"},"Target":"_self","Context":"com.sun.star.text.TextDocument"}))
        i += 1
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(dic,{"URL":"private:separator"}))
        i += 1
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(dic,{"URL":"","Title":{"en-US":"Add-On sub menu"},"Target":"_self","Submenu":["m1",self.subMenu2]}))      
        return nd
    def subMenu2(self,dic,val):
        nd = Elem("node",{"oor:name":"Submenu"})  # 変更不可。
        i = 0
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function2","Title":{"en-US":"Add-On Function 2"},"Target":"_self","Context":"com.sun.star.sheet.SpreadsheetDocument"}))
        return nd
class OfficeToolBar(MenuItem):  # ツールバーを作成。
    '''
    OfficeToolBar
    View->Toolbars
    Select this tool bar.
    
    ツールバーの名前は未設定。
    
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"OfficeToolBar"})  # 変更不可。 
        self.append(Elem("node",{'oor:name':dic["HANDLED_PROTOCOL"],"oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。
        self[0].append(Elem("node",{'oor:name':"m1","oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。  
        self[0][0].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function1","Title":{"en-US":"Function 1"},"Target":"_self","Context":"com.sun.star.text.TextDocument"}))
        self[0].append(Elem("node",{'oor:name':"m2","oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。 
        self[0][1].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function2","Title":{"en-US":"Function 2"},"Target":"_self","Context":"com.sun.star.text.TextDocument"}))
        self.createWindwStatexcu(dic,"Writer")  # Writer用のツールバーのプロパティの設定。
    def createWindwStatexcu(self,dic,ctxt):  # ツールバーのプロパティの設定。
        #Creation of WriterWindwState.xcu、Calcの場合はCalcWindwState.xcu
        filename = ctxt + "WindowState.xcu"
        createBK(filename)  # すでにあるファイルをbkに改名
        with open(filename,"w",encoding="utf-8") as fp:   
            rt = Elem("oor:component-data",{"oor:name":ctxt + "WindowState","oor:package":"org.openoffice.Office.UI","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema"})  # 根の要素を作成。
            rt.append(Elem("node",{'oor:name':"UIElements"}))
            rt[0].append(Elem("node",{'oor:name':"States"}))
            rt[0][0].append(Elem("node",{'oor:name':"private:resource/toolbar/addon_" + dic["HANDLED_PROTOCOL"],"oor:op":"replace"}))
            rt[0][0][0].extend(super().createWindowStateNodes(dic,{"UIName":{"en-US":"OfficeToolBar Title"},"ContextSensitive":"false","Visible":"true","Docked":"false"}))  # ツールバーのプロパティを設定。
            tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
            tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
            print(filename + " has been created.")  
class Images(MenuItem):  # アイコンを表示させるコマンドURLを設定。
    '''
    Specify command URL to display icon
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"Images"})  # 変更不可。  
        # 画像1
        name = "com.sun.star.comp.framework.addon.image1"  # oor:nameの値はノードの任意の固有名。
        url = dic["HANDLED_PROTOCOL"] + ":Function1"  # アイコンを表示させるコマンドURL
        dic_image = {
            "ImageSmallURL":"%origin%/icons/image1ImageSmall.png",
            "ImageBigURL":"%origin%/icons/image1ImageBig.png",
            }
        self.append(self.userDefinedImages(name,url,dic_image))
        # 画像2
        name = "com.sun.star.comp.framework.addon.image2"  # oor:nameの値はノードの任意の固有名。
        url = "org.openoffice.Office.addon.example:Help"  # アイコンを表示させるコマンドURL
        dic_image = {
            "ImageSmallURL":"%origin%/icons/image2ImageSmall.png",
            "ImageBigURL":"%origin%/icons/image2ImageBig.png",
            }        
        self.append(self.userDefinedImages(name,url,dic_image))
    def userDefinedImages(self,name,url,dic_image):  
        '''
        アイコンの設定。
        
        :param name: name of icon
        :type name: str
        :param url: uri of icon
        :type url: str
        :param dic_image:  a dictionary of the same image with different sizes
        :type dic_image: dict
        :returns: a node for an image
        :rtype: xml.etree.ElementTree.Element
        '''
        nd = Elem("node",{"oor:name":name,"oor:op":"replace"})  # oor:nameの値はノードの任意の固有名。
        nd.append(Elem("prop",{"oor:name":"URL"}))
        nd[0].append(Elem("value",text=url))  # アイコンを表示させるコマンドURLを設定。
        nd.append(Elem("node",{"oor:name":"UserDefinedImages"}))
        ORDER = "ImageSmall","ImageBig","ImageSmallHC","ImageBigHC"
        for key in ORDER:
            if key in dic_image:
                snd = Elem("prop",{"oor:name":key,"oor:type":"xs:hexBinary"})
                snd.append(Elem("value",text=dic_image[key]))
                nd[1].append(snd)
        ORDER = "ImageSmallURL","ImageBigURL"  # "ImageSmallHCURL","ImageBigHCURL" valueノードのテキストノードの空白があると画像が表示されない。HC画像が優先して表示されてしまうのでHC画像は使わない。
        for key in ORDER:
            if key in dic_image:
                snd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                snd.append(Elem("value",text=dic_image[key]))
                nd[1].append(snd)        
        return nd
class OfficeHelp(MenuItem):  # ヘルプメニューの設定。 
    '''
    Help Menu
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"OfficeHelp"})  # 変更不可。  
        self.append(Elem("node",{'oor:name':"com.sun.star.comp.framework.addon","oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。           
        self[0].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Help","Title":{"x-no-translate":"","de":"Über Add-On Beispiel","en-US":"About Add-On Example"},"Target":"_self"}))
def main():
    #Creation of ProtocolHandler.xcu
    os.chdir(src_path)  # srcフォルダに移動。
    for dic in LST:  # 設定リストの各辞書について
        if "HANDLED_PROTOCOL" in dic:  # HANDLED_PROTOCOLが辞書のキーにあるとき
            filename =  "ProtocolHandler.xcu"
            createBK(filename)  # すでにあるファイルをbkに改名
            with open(filename,"w",encoding="utf-8") as fp:
                rt = Elem("oor:component-data",{"oor:name":"ProtocolHandler","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema","xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。
                rt.append(Elem("node",{'oor:name':"HandlerSet"}))
                rt[0].append(Elem("node",{'oor:name':dic["IMPLE_NAME"],"oor:op":"replace"}))
                rt[0][0].append(Elem("prop",{'oor:name':"Protocols","oor:type":"oor:string-list"}))
                rt[0][0][0].append(Elem("value",text = dic["HANDLED_PROTOCOL"] + ":*"))
                tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
                tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
                print(filename + " has been created.")    
            #Creation of Addons.xcu
            filename =  "Addons.xcu"
            createBK(filename)  # すでにあるファイルをbkに改名
            with open(filename,"w",encoding="utf-8") as fp:   
                rt = Elem("oor:component-data",{"oor:name":"Addons","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema"})  # 根の要素を作成。
                rt.append(Elem("node",{'oor:name':"AddonUI"}))
                rt[0].extend([AddonMenu(dic),OfficeMenuBar(dic),OfficeToolBar(dic),Images(dic),OfficeHelp(dic)])  # 追加するノード。
                tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
                tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
                print(filename + " has been created.")  
if __name__ == "__main__":
    sys.exit(main())