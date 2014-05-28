import maya.cmds as mc
import pymel.core as py
import maya.mel as mel

class ecSDK(object):
    def __init__(self):
        self.window = 'sdkflip'
        self.title = 'ec Set Driven Key Utility'
        self.width_height = (312, 289)

        if py.window(self.window, exists=True):
            py.deleteUI(self.window)
        py.window(self.window, title=self.title, wh=self.width_height, sizeable=False)
        py.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
        py.rowLayout("objRow", numberOfColumns=4, columnAlign2=("left", "right"), p="sdkflip")
        py.columnLayout("objCol", p="objRow")
        self.source_field = py.textField("sourceText", tx="Source Driver", p="objCol")
        py.columnLayout("objbutCol", p="objRow")
        py.button(label="<<", width=30, height=20, p="objbutCol", bgc=(0.8, 0.8, 0.8), command=py.Callback(self.ec_gui_fun, "sourcetxt"))
        py.columnLayout("tarCol", p="objRow")
        self.target_field = py.textField("targetText", tx="Target Driver", p="tarCol")
        py.columnLayout("tarbutCol", p="objRow")
        py.button(label="<<", width=30, height=20, p="tarbutCol", bgc=(0.8, 0.8, 0.8), command=py.Callback(self.ec_gui_fun, "targettxt"))
        py.frameLayout("scrollFrame", label="Driver Attributes", cll=False, borderStyle="etchedIn", p="sdkflip")
        py.rowLayout("scrollRow", p="scrollFrame")
        self.scroll_list = py.textScrollList("attrList", w=300, h=200, numberOfRows=8, allowMultiSelection=True, p="scrollRow")
        py.rowLayout("comRow", numberOfColumns=4, p="sdkflip")
        py.text("preText", l="Target Prefix", p="comRow")
        self.prefix_field = py.textField("prefixText", tx="rt", w=70, p="comRow")
        py.button(label="Mirror", width=80, height=30, p="comRow", bgc=(0.8, 0.8, 0.8), command=py.Callback(self.ec_sdk_flip, True))
        py.button(label="Copy", width=80, height=30, p="comRow", bgc=(0.8, 0.8, 0.8), command=py.Callback(self.ec_sdk_flip, False))

        py.showWindow(self.window)

    def ec_gui_fun(self, operation):
        try:
            sel = mc.ls(sl=True)
            if operation == "sourcetxt":
                self.source_field.setText(sel[0])
                attr = mc.listAttr(sel[0], r=True, v=True, k=True, hd=True)
                self.scroll_list.removeAll().append(attr)
            elif operation == "targettxt":
                self.target_field.setText(sel[0])
        except IndexError:
            mc.warning("Must have an object selected!")

    def ec_sdk_flip(self, mirror):
        driver = self.source_field.getText()
        drive_channel = self.scroll_list.getSelectItem()
        m_driver = self.target_field.getText()
        m_side = self.prefix_field.getText()
        duplicate_sdk = {}
        animation_curves = ''
        done_nodes = []
        for i in range(0, len(drive_channel)):
            #get connections to driver
            sdk_nodes = mc.listConnections(driver + "." + drive_channel[i], source=False, scn=True)
            if not sdk_nodes != None:
                mc.warning('must have object thing selected yeah')
            else:
                #select nodes and store only the SDK's
                mc.select(sdk_nodes)
                animation_curves = mc.ls(sl=True, type=("animCurveUL","animCurveUU","animCurveUA","animCurveUT"))
                for curve in animation_curves:
                    if curve in done_nodes:
                        pass
                    else:
                        duplicate_sdk[curve] = mc.duplicate(curve)
                        mc.connectAttr(m_driver+"."+ drive_channel[i], duplicate_sdk[curve][0]+".input")
        for f in range(0, len(animation_curves)):
            #for every sdk node connected to anim curve, check the target
            target = mc.listConnections(animation_curves[f]+'.output', source=True, p=True, scn=True)
            #if the target is a blendWeighted node:
            if 'blend' in target[0]:
                mc.warning(target[0])
                blend_object, attr = target[0].split('.')
                #get output of blendWeighted node
                blend_connections = mc.listConnections(blend_object, source=False, p=True, scn=True)
                #get inputs of blendWeighted node
                blend_inputs = mc.listConnections(blend_object, source=True, scn=False, type='animCurveUL')
                blend_inputs.append(mc.listConnections(blend_object, source=True, scn=False, type='animCurveUU'))
                blend_inputs.append(mc.listConnections(blend_object, source=True, scn=False, type='animCurveUA'))
                blend_inputs.append(mc.listConnections(blend_object, source=True, scn=False, type='animCurveUT'))
                m_blend = mc.duplicate(blend_object)
                m_driven = m_side + blend_connections[0][len(m_side):]
                mc.connectAttr(m_blend[0]+".output",  m_driven)

                for l in range(0, len(blend_inputs)):
                    if not blend_inputs[l] != None:
                        pass
                    else:
                        if blend_inputs[l] in done_nodes:
                            mc.connectAttr(duplicate_sdk[blend_inputs[l]][0]+'.output', m_blend[0]+'.input[%i]' % l)
                            mc.delete(m_blend)
                        else:
                            mc.connectAttr(duplicate_sdk[blend_inputs[l]][0]+'.output', m_blend[0]+'.input[%i]' % l)
                            done_nodes.append(blend_inputs[l])
                        if mirror is True:
                            mel.eval("scaleKey -time \":\" -float \":\" -valueScale -1 (\""+duplicate_sdk[animation_curves[f]][0]+"\");")
                        mc.rename(duplicate_sdk[blend_inputs[l]][0], (m_driven+duplicate_sdk[blend_inputs[l]][0][len(m_driven):]))
            else:
                m_driven_obj, attr = mc.listConnections(animation_curves[f], source=False, p=True, scn=True)[0].split('.')
                #driven_inputs = mc.listConnections(mdrivenobj, source=True, scn=False, type='transform')
                m_driven = m_side + m_driven_obj[len(m_side):]
                mc.connectAttr(duplicate_sdk[animation_curves[f]][0]+".output",  m_driven + '.' + attr)
                if mirror is True:
                    mel.eval("scaleKey -time \":\" -float \":\" -valueScale -1 (\""+duplicate_sdk[animation_curves[f]][0]+"\");")
                mc.rename(duplicate_sdk[animation_curves[f]][0], (m_driven+duplicate_sdk[animation_curves[f]][0][len(m_driven):]))
                    
sdk_instance = ecSDK()