#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
IMPLE_NAME = "UnoInsp"
SERVICE_NAME = "com.blogspot.pq.UnoInsp"
def create(ctx, *args):
    try:
        import component
        return component.create(IMPLE_NAME, ctx, *args)
    except Exception as e:
        print(e)
# Registration
import unohelper
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(create, IMPLE_NAME, (SERVICE_NAME,),)
