__author__ = 'Evan Cox: coxevan90@gmail.com'
import pymel.core as py
import maya.mel as mel

def ec_face_mirror_gui():
    win_name = 'facemirrorgui'
    title = 'Face Mirror'
    size = (148, 84)
    if py.window(win_name, exists=True):
        py.deleteUI(win_name, window=True)
    window = py.window(win_name, title=title, widthHeight=size, menuBar=True, sizeable=False)
    face_frame = py.frameLayout('ctrl_frame', l='Mirror Faces', p=win_name)
    face_row = py.rowLayout(p=face_frame, numberOfColumns=2)
    face1_col = py.columnLayout('face1_col', p=face_row)
    face2_col = py.columnLayout('face2_col', p=face_row)
    py.button('nameButton', l='>>', c=py.Callback(check_tx), p=face1_col)
    py.textField('nameText', tx='Name of Mesh', p=face2_col)
    face2_row = py.rowLayout(p=face_frame, numberOfColumns=2)
    py.button('mirrorButton', l='Mirror Selection', p=face2_row, c=py.Callback(ec_face_mirror))
    py.popupMenu(p='mirrorButton', ctl=False, button=3)
    py.menuItem(l='Mirror XY', command=py.Callback(ec_face_mirror, axis='sz'))
    py.menuItem(l='Mirror YZ', command=py.Callback(ec_face_mirror, axis='sx'))
    py.menuItem(l='Mirror XZ', command=py.Callback(ec_face_mirror, axis='sy'))
    py.button('helpButton', l='Help', p=face2_row, c=py.Callback(ec_face_help))

    py.showWindow(window)

def check_tx():
    try:
        name = py.ls(sl=True)
        py.textField('nameText', e=True, tx=name[0])
    except IndexError:
        py.warning('Must have at least one object selected!')

def ec_face_mirror(**kwargs):
    attr = kwargs.setdefault('axis', 'sx')
    obj = py.textField('nameText', q=True, tx=True)
    sel = py.ls(sl=True)
    py.polyChipOff(sel, dup=True)
    temp_obj = py.polySeparate(obj, n='tempObj')

    py.setAttr('%s.%s' % (temp_obj[1], attr), -1)
    py.select(temp_obj)
    temp_obj[0] = py.polyUnite(temp_obj, ch=False)
    py.rename(temp_obj[0], obj)
    mel.eval('ConvertSelectionToVertices;')
    py.polyMergeVertex()

def ec_face_help():
    win_name = 'facemirrorhelp'
    title = 'Face Mirror: Help!'
    size = (359, 75)
    if py.window(win_name, exists=True):
        py.deleteUI(win_name, window=True)
    window = py.window(win_name, title=title, widthHeight=size, menuBar=True, sizeable=False)
    help_row = py.rowLayout('helprow')
    py.text('How to use this tool: \n\
    1) Select the mesh you\'d like to mirror part of and click the >> button\n\
    2) Select the faces of the mesh you\'d like to mirror\n\
    3) Click the Mirror Selection button!\n\
    4) Right clicking the Mirror Selection button gives you additional options', al='left')
    py.showWindow(win_name)

ec_face_mirror_gui()

