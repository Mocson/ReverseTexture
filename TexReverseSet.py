import pymel.core as pm
import maya.cmds as cmds

# 処理部========================================

# マテリアル選択→取得
def secmat():
    global mat
    objs = pm.ls(sl=True)
    SG = pm.listConnections(objs, s=False, d=True, t='shadingEngine')
    mat = pm.ls(pm.listConnections(SG, s=True, d=False), mat=True)
    test = ''.join(mat[0])
    cmds.textField('tFld', edit=True, text=test)

# Deffuse----------------
def createRev():
    NowRev = pm.shadingNode( 'reverse', asUtility=True, n='RevTex')
    NowTex = pm.shadingNode( 'file', asTexture=True, isColorManaged=True, n='RevFile')
    pm.connectAttr(NowRev+'.outputX', mat[0]+'.colorR' , f=True)
    pm.connectAttr(NowRev+'.outputY', mat[0]+'.colorG' , f=True)
    pm.connectAttr(NowRev+'.outputZ', mat[0]+'.colorB' , f=True)
    pm.connectAttr(NowTex+'.outColorR', NowRev+'.inputX', f=True)
    pm.connectAttr(NowTex+'.outColorG', NowRev+'.inputY', f=True)
    pm.connectAttr(NowTex+'.outColorB', NowRev+'.inputZ', f=True)

# Specular----------------
def createSpec():
    NowSpec = pm.shadingNode( 'reverse', asUtility=True, n='RevSpec')
    NowTexC = pm.shadingNode( 'file', asTexture=True, isColorManaged=True, n='Revfile')
    pm.connectAttr(NowTexC+'.outAlpha', NowSpec+'.inputX' , f=True)
    pm.connectAttr(NowSpec+'.outputX' , mat[0]+'.specularRoughness' , f=True)

# Bump Map----------------
def createBump():
    NowRevB = pm.shadingNode( 'reverse', asUtility=True, n='RevTex')
    NowBump = pm.shadingNode( 'bump2d', asUtility=True, n='RevBump')
    NowTexB = pm.shadingNode( 'file', asTexture=True, isColorManaged=True, n='RevFile')
    pm.connectAttr(NowTexB+'.outAlpha', NowRevB+'.inputX' , f=True)
    pm.connectAttr(NowRevB+'.outputX', NowBump+'.bumpValue' , f=True)
    pm.connectAttr(NowBump+'.outNormal',  mat[0]+'.normalCamera' , f=True)


# ウィンドウ部------------------------------
cmds.window(title='ReverseTextures', w=300)
cmds.columnLayout(adj=True)
cmds.button( label = 'Select Material', w=200, h=40, command='secmat()')
cmds.textField('tFld')

cmds.separator( h=10 )
cmds.text("Diffuse")
cmds.separator( h=10 )
cmds.button( label = 'Set', w=200, h=40, command='createRev()')

cmds.separator( h=10 )
cmds.text("Bump")
cmds.separator( h=10 )
cmds.button( label = 'Set', w=200, h=40, command='createBump()')

cmds.separator( h=10 )
cmds.text("Specular")
cmds.separator( h=10 )
cmds.button( label = 'Set', w=200, h=40, command='createSpec()')

cmds.showWindow()
