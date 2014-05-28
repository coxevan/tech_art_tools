import maya.mel as mel
import pymel.core as py
import os
from PIL import Image

class ReferencePlane(object):
    def __init__(self):
        self.window = "refWindow"
        self.title = "ec Reference Creator"
        self.width_height = (460, 220)
        self.image_height = 0
        self.image_width = 0

        if py.window(self.window, ex=True):
            py.deleteUI(self.window)
        buhi = 30
        py.window(self.window, menuBar=True, title=self.title, widthHeight=self.width_height, sizeable=False)
        py.frameLayout("standardFrame", label="Reference Creator", collapsable=False, borderStyle="etchedIn")
        py.rowLayout("standardRow", numberOfColumns=4, columnAlign4=("left", "center", "right", "right"), \
                     p="standardFrame")
        py.columnLayout("standardCol1", p="standardRow")
        py.text("1) Name your reference")
        self.reference_name = py.textField("refField", tx="Reference_Name")
        py.text("2) Find your image")
        py.button(w=130, h=buhi, p="standardCol1", label="Import Image", c=py.Callback(self.ecRefSize))
        py.text("Image Path")
        self.image_path = py.textField("imgField", tx="//")
        py.text("Alpha Value (0 - 1.0)")
        self.alpha_value = py.textField("alpha_value_field", tx="0.5")
        py.text("Reference Scale Factor")
        self.scalefactor_field = py.textField("imgHeight", tx=".1")

    
        py.columnLayout("standardCol2", p="standardRow")
        self.image_preview = py.image("thumb", w=320, h=140)
        self.radio_grp = py.radioButtonGrp("refRadio", sl=1, nrb=3, l="3) Orient:", p="standardCol2", cal=(1, "left"),\
                                           cw4=(50, 70, 100, 80), la3=("X (Side)", "Y (Top/Bottom)", "Z (Front/Back)"))
        creation_button = py.button(w=320, h=buhi, p="standardCol2", label="4) Make Reference Plane with selected Image",\
                  c=py.Callback(self.ecRefPlane, False))
        py.popupMenu(p=creation_button, ctl=False, button=3)
        #py.menuItem(l='', command=py.Callback(self.ecRefPlane, False))
        py.menuItem(l='Flip Axis', command=py.Callback(self.ecRefPlane, True))
    
        py.showWindow(self.window)
    
    def ecRefPlane(self, flip):
        scale_factor = float(self.scalefactor_field.getText())
        material = self.ecApplyMat()
        name = self.reference_name.getText()
        radio = self.radio_grp.getSelect()

        height = float(self.image_height) * scale_factor
        width = float(self.image_width) * scale_factor
        if flip is True:
            if radio == 3:
                names = py.polyPlane(n=name, ax=(0, 0, 1), w=width, h=height, sx=1, sy=1)
                py.setAttr(names[0]+'.scaleX', -1)
                py.move(0, (.5*height), 0, names[0])
            elif radio == 2:
                names = py.polyPlane(n=name, ax=(0, 1, 0), w=width, h=height, sx=1, sy=1)
                py.setAttr(names[0]+'.scaleZ', -1)
            else:
                names = py.polyPlane(n=name, ax=(1, 0, 0), w=width, h=height, sx=1, sy=1)
                py.setAttr(names[0]+'.scaleZ', -1)
                py.move(0, (.5*height), 0, names[0])
        else:
            if radio == 3:
                names = py.polyPlane(n=name, ax=(0, 0, 1), w=width, h=height, sx=1, sy=1)
                py.move(0, (.5*height), 0, names[0])
            elif radio == 2:
                names = py.polyPlane(n=name, ax=(0, 1, 0), w=width, h=height, sx=1, sy=1)
            else:
                names = py.polyPlane(n=name, ax=(1, 0, 0), w=width, h=height, sx=1, sy=1)
                py.move(0, (.5*height), 0, names[0])

        py.select(names)
        py.hyperShade(assign=material)
        py.delete(ch=True)
        py.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        py.select(cl=True)

        layer = "Ref_Layer"
        if py.objExists(layer) is False:
            py.createDisplayLayer(empty=True, n=layer)
            py.setAttr(layer+".dt", 2)
        py.editDisplayLayerMembers(layer, names[0])

    def ecApplyMat(self):
        material = py.shadingNode("lambert", asShader=True, n="refMaterial")
        alpha_value = self.alpha_value.getText()
        alpha_value = float(alpha_value)
        SG = py.sets(material, renderable=True, noSurfaceShader=True, empty=True)
        py.connectAttr((material + ".outColor"), (SG + ".surfaceShader"), f=True)
        py.setAttr((material+".transparency"), alpha_value, alpha_value, alpha_value, type="double3")

        filepath = self.image_path.getText()
        img = py.shadingNode('file', asTexture=True)
        py.setAttr(img+'.fileTextureName', filepath, type='string')
        py.connectAttr(img+'.outColor', material+'.color', force=True)
        return material

    def ecRefSize(self):
        file_path = py.fileDialog(title="Find your image!")
        image_plane_name = py.createNode("imagePlane")
        py.setAttr( "%s.imageName" % image_plane_name, file_path, type="string")
        file_size = py.imagePlane(image_plane_name, q=True, imageSize=True)
        py.delete("imagePlane1")

        self.image_path.setText(file_path)
        self.image_width = file_size[0]
        self.image_height = file_size[1]

        size = 128, 128
        dir, ext = os.path.splitext(file_path)
        new_image = dir+'_thumbnail.png'
        im = Image.open(file_path)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(new_image, "PNG")
        self.image_preview.setImage(new_image)

reference_instance = ReferencePlane()