import maya.cmds as mc
import pymel.core as py


def ec_zero_gui():
    if mc.window("zero", ex=True):
        mc.deleteUI("zero")
    buhi = 30
    mc.window("zero", menuBar=True, title="Zero Channels", widthHeight=(460, 122), sizeable=False)
    mc.frameLayout("standardFrame", label="Standard Attributes", collapsable=False, borderStyle="etchedIn")
    mc.rowLayout("standardRow", numberOfColumns=4, columnAlign4=("left", "center", "right", "right"), p="standardFrame")
    mc.columnLayout("standardCol1", p="standardRow")
    translate = mc.button(w=110, h=buhi, p="standardCol1", label="Translate", c=py.Callback(ec_zero, 't'))
    t_pop = mc.popupMenu(p=translate)
    mc.menuItem(l='Translate X', p=t_pop, c=py.Callback(ec_zero, 'tx'))
    mc.menuItem(l='Translate Y', p=t_pop, c=py.Callback(ec_zero, 'ty'))
    mc.menuItem(l='Translate Z', p=t_pop, c=py.Callback(ec_zero, 'tz'))

    mc.columnLayout("standardCol2", p="standardRow")
    rotate = mc.button(w=110, h=buhi, p="standardCol2", label="Rotate", c=py.Callback(ec_zero, 'r'))
    r_pop = mc.popupMenu(p=rotate)
    mc.menuItem(l='Rotate X', p=t_pop, c=py.Callback(ec_zero, 'rx'))
    mc.menuItem(l='Rotate Y', p=t_pop, c=py.Callback(ec_zero, 'ry'))
    mc.menuItem(l='Rotate Z', p=t_pop, c=py.Callback(ec_zero, 'rz'))
 
    mc.columnLayout("standardCol3", p="standardRow")
    scale = mc.button(w=110, h=buhi, p="standardCol3", label="Scale", c=py.Callback(ec_zero, 's'))
    s_pop = mc.popupMenu(p=scale)
    mc.menuItem(l='Scale X', p=t_pop, c=py.Callback(ec_zero, 'sx'))
    mc.menuItem(l='Scale Y', p=t_pop, c=py.Callback(ec_zero, 'sy'))
    mc.menuItem(l='Scale Z', p=t_pop, c=py.Callback(ec_zero, 'sz'))
 
    mc.columnLayout("standardCol4", p="standardRow")
    mc.button(w=110, h=buhi, p="standardCol4", label="All Keyable", c=py.Callback(ec_zero, 'all'))
 
    mc.frameLayout("extraFrame", label="Extra Attributes", collapsable=False, borderStyle="etchedIn", p="zero")
    mc.rowLayout("extraRow", numberOfColumns=5, p="extraFrame")
    mc.columnLayout("extraCol1", p="extraRow")
    mc.textField("attrField", p="extraCol1", tx="Attribute Name")
    buwi = 80
    mc.columnLayout("extraCol2", p="extraRow")
    mc.button(w=buwi, h=buhi, p="extraCol2", label="Zero", c=py.Callback(ec_custom_zero, 'zero'))
    mc.columnLayout("extraCol3", p="extraRow")
    mc.button(w=buwi, h=buhi, p="extraCol3", label="Min", c=py.Callback(ec_custom_zero, 'min'))
    mc.columnLayout("extraCol4", p="extraRow")
    mc.button(w=buwi, h=buhi, p="extraCol4", label="Max", c=py.Callback(ec_custom_zero, 'max'))
    mc.columnLayout("extraCol5", p="extraRow")
    mc.button(w=buwi, h=buhi, p="extraCol5", label="Default", c=py.Callback(ec_custom_zero, 'def'))
    mc.showWindow("zero")


def ec_zero(attr="all"):
    selection = mc.ls(sl=True, type='transform')
    try:
        if attr == "sx" or attr == "sy" or attr == "sz":
            for i in range(0, len(selection)):
                mc.setAttr(selection[i]+"."+attr, 1.0)
        elif attr == "s":
            for i in range(0, len(selection)):
                mc.setAttr(selection[i]+"."+attr, 1, 1, 1, type="double3")
        elif attr == "all":
            for i in range(0, len(selection)):
                listat = mc.listAttr(selection[i], v=True, k=True)
                print "listat :"
                if listat is None:
                    print "ERROR: listat is None : %s" % selection[i]
                else:
                    for k in range(0, len(listat)):
                        if listat[k] == "scaleX" or listat[k] == "scaleY" or listat[k] == "scaleZ" or listat[k] == "scale" or\
                                        listat[k] == "visibility":
                            mc.setAttr(selection[i]+"."+listat[k], 1.0)
                        else:
                            mc.setAttr(selection[i]+"."+listat[k], 0.0)
        else:
            if attr == "t" or attr == "r":
                for i in range(0, len(selection)):
                    mc.setAttr(selection[i]+"."+attr, 0.0, 0.0, 0.0, type="double3")
            else:
                for i in range(0, len(selection)):
                    mc.setAttr(selection[i]+"."+attr, 0.0)
        py.headsUpMessage("Reset: %s attribute of object %s" % (attr, selection))
    except:
        py.warning("ERROR: %s attribute of %s is locked or otherwise unavailable to reset" % (attr, selection[i]))


def ec_custom_zero(operation):
    selection = mc.ls(sl=True)
    attr = mc.textField("attrField", q=True, tx=True)
    if operation == "zero":
        for i in range (0, len(selection)):
            mc.setAttr(selection[i] + "." + attr, 0)
    elif operation == "min":
        for i in range(0, len(selection)):
            minValue = mc.attributeQuery(attr, node=selection[i], min=True)
            mc.setAttr(selection[i] + "." + attr, minValue[0])
    elif operation == "max":
        for i in range(0, len(selection)):
            maxValue = mc.attributeQuery(attr, node=selection[i], max=True)
            mc.setAttr(selection[i] + "." + attr, maxValue[0])
    elif operation == "def":
        for i in range(0, len(selection)):
            defValue = mc.attributeQuery(attr, node=selection[i], ld=True)
            mc.setAttr(selection[i] + "." + attr, defValue[0])

ec_zero_gui()