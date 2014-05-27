import pymel.core as py
import maya.cmds as mc
import classes as cl
import os
import connections as con
reload(con)
reload(cl)


def show_group(shown_group):
    group_image = {'up_eye_locator_grp': 'thumb_upeye.png',
                   'low_eye_locator_grp': 'thumb_loweye.png',
                   'up_lip_locator_grp': 'thumb_upmouth.png',
                   'low_lip_locator_grp': 'thumb_lowmouth.png',
                   'head_locator_grp': 'thumb_jaw_head.png',
                   'cheek_locator_grp': 'thumb_cheek.png'}

    if shown_group == 'all':
        py.showHidden('up_eye_locator_grp',
                'low_eye_locator_grp',
                'up_lip_locator_grp',
                'low_lip_locator_grp',
                'head_locator_grp',
                'cheek_locator_grp')
    else:
        py.hide('up_eye_locator_grp',
                'low_eye_locator_grp',
                'up_lip_locator_grp',
                'low_lip_locator_grp',
                'head_locator_grp',
                'cheek_locator_grp')
        py.showHidden(shown_group)
        guide_gui(group_image[shown_group])


def get_file_path(filename):
    file_path = __file__
    dir_path = file_path[:-15]
    base_path = os.path.join(dir_path, filename)
    return base_path


def import_file():
    base_path = get_file_path('ecAutoFaceImport.mb')
    if mc.objExists('Blend_Morph') is False:
        mc.file(base_path, i=True)
        py.hide('baseoffset', 'PhonemeController')
    else:
        pass
    

def face_mesh_query():
    transforms = []
    transforms.append(py.getAttr('Blend_Morph.translate'))
    transforms.append(py.getAttr('Blend_Morph.rotate'))
    transforms.append(py.getAttr('Blend_Morph.scale'))
    py.setAttr('master_locator_grp.translate', transforms[0], type="double3")
    py.setAttr('master_locator_grp.rotate', transforms[1], type="double3")
    py.setAttr('master_locator_grp.scale', transforms[2], type="double3")

    py.setAttr('master_offset_grp.translate', transforms[0], type="double3")
    py.setAttr('master_offset_grp.rotate', transforms[1], type="double3")
    py.setAttr('master_offset_grp.scale', transforms[2], type="double3")
    py.hide('Blend_Morph')


def face_set_up():
    py.deleteUI('face_placement_prompt', window=True)
    group_list = ['master_locator_grp',
              'up_eye_locator_grp',
              'low_eye_locator_grp',
              'cheek_locator_grp',
              'up_lip_locator_grp',
              'low_lip_locator_grp',
              'head_locator_grp',
              'master_offset_grp']

    for group in group_list:
        inst_group = cl.EcGroup(groupName=group)
        inst_group.set_parent()
        inst_group.create_locators()
    face_mesh_query()
    locator_placement_gui()
    
    
def start_gui():
    window = 'face_placement_prompt'
    window_title = 'ecFaceSetup Face Prompt!'
    if py.window(window, exists=True):
        py.deleteUI(window, window=True)
    if py.window('locator_placement_prompt', exists=True):
        py.deleteUI('locator_placement_prompt', window=True)
    if py.window('guide_gui', exists=True):
        py.deleteUI('guide_gui', window=True)
    if py.window('offset_gui', exists=True):
        py.deleteUI('offset_gui', window=True)
    window_obj = py.window(window, title=window_title, widthHeight=(100, 100), sizeable=True)
    py.rowLayout('prompt_row', p=window)
    py.columnLayout('prompt_column', p='prompt_row')
    py.text('Manipulate the new face mesh transform/rotate/scale to fit the face of your character\n\
            then click next!', p='prompt_column')
    py.button('face_placement_button', label='Next', p='prompt_column', command=py.Callback(face_set_up))
    py.showWindow(window)


def locator_placement_gui():
    window = 'locator_placement_prompt'
    window_title = 'ecFaceSetup'
    window_size = (337, 245)
    button_width = 130
    if py.window(window, exists=True):
        py.deleteUI(window, window=True)
    if py.window('guide_gui', exists=True):
        py.deleteUI('guide_gui', window=True)
    if py.window('offset_gui', exists=True):
        py.deleteUI('offset_gui', window=True)

    window_obj = py.window(window, title=window_title, widthHeight=window_size, menuBar=True, sizeable=False)
    menu = py.menu('File', p=window_obj)
    py.menuItem('Reset All', p=menu, command=py.Callback(reset_locators, 'all'))
    py.menuItem(divider=True, p=menu)
    mirror = py.menuItem('Mirroring', p=menu, subMenu=True)
    py.menuItem('Mirror All', p=mirror, command=py.Callback(mirror_locators, filename='all'))
    py.menuItem(divider=True, p=menu)
    py.menuItem('Mirror Upper Eyes', p=mirror, command=py.Callback(mirror_locators, filename='up_eye'))
    py.menuItem('Mirror Lower Eyes', p=mirror, command=py.Callback(mirror_locators, filename='low_eye'))
    py.menuItem('Mirror Cheek', p=mirror, command=py.Callback(mirror_locators, filename='cheek'))
    py.menuItem('Mirror Upper Lip', p=mirror, command=py.Callback(mirror_locators, filename='up_mouth'))
    py.menuItem('Mirror Lower Lip', p=mirror, command=py.Callback(mirror_locators, filename='low_mouth'))
    py.menuItem('Remove Mirroring', p=mirror, command=py.Callback(mirror_locators, unmirror=True))
    py.menuItem(divider=True, p=menu)
    py.menuItem('Delete Everything', p=menu, command=py.Callback(delete_locators))
    py.menuItem(divider=True, p=menu)

    py.columnLayout('god_column', p=window)
    py.rowLayout('master_row', numberOfColumns=5, p='god_column')
    py.columnLayout('master_column', p='master_row', cat=('left', 0))
    py.rowLayout('jaw_row', p='master_column', numberOfColumns=3)
    jaw_btn = py.button('jaw_btn', label='Place Head Locators', w=button_width,  p='jaw_row',
              command=(py.Callback(show_group, 'head_locator_grp')))
    jaw_menu = py.popupMenu('jaw_menu', p=jaw_btn, ctl=False, button=3)
    py.menuItem('Reset Locators', p=jaw_menu, command=py.Callback(reset_locators, 'head_locator_grp'))
    py.button('jaw_guide_button', label='Guide', p='jaw_row', command=py.Callback(guide_gui, 'jaw_head.png', full=True))

    py.rowLayout('u_eye_row', p='master_column', numberOfColumns=3)
    u_eye_btn = py.button('u_eye_btn', label='Place Upper Eye Locators', w=button_width,  p='u_eye_row',
              command=(py.Callback(show_group, 'up_eye_locator_grp')))
    u_eye_menu = py.popupMenu('u_eye_menu', p=u_eye_btn, ctl=False, button=3)
    py.menuItem('Reset Locators', p=u_eye_menu, command=py.Callback(reset_locators, 'up_eye_locator_grp'))
    py.button('u_eye_guide_button', label='Guide', p='u_eye_row', command=py.Callback(guide_gui, 'upeye.png', full=True))

    py.rowLayout('l_eye_row', p='master_column', numberOfColumns=3)
    l_eye_btn = py.button('l_eye_btn', label='Place Lower Eye Locators', w=button_width,  p='l_eye_row',
              command=(py.Callback(show_group, 'low_eye_locator_grp')))
    l_eye_menu = py.popupMenu('l_eye_menu', p=l_eye_btn, ctl=False, button=3)
    py.menuItem('Reset Locators', p=l_eye_menu, command=py.Callback(reset_locators, 'low_eye_locator_grp'))
    py.button('l_eye_guide_button', label='Guide', p='l_eye_row', command=py.Callback(guide_gui, 'loweye.png', full=True))

    py.rowLayout('cheek_row', p='master_column', numberOfColumns=3)
    cheek_btn = py.button('cheek_btn', label='Place Cheek Locators', w=button_width,  p='cheek_row',
              command=(py.Callback(show_group, 'cheek_locator_grp')))
    cheek_menu = py.popupMenu('cheek_menu', p=cheek_btn, ctl=False, button=3)
    py.menuItem('Reset Locators', p=cheek_menu, command=py.Callback(reset_locators, 'cheek_locator_grp'))
    py.button('cheek_guide_button', label='Guide', p='cheek_row', command=py.Callback(guide_gui, 'cheek.png', full=True))

    py.rowLayout('u_lip_row', p='master_column', numberOfColumns=3)
    u_lip_btn = py.button('u_lip_btn', label='Place Upper Lip Locators', w=button_width,  p='u_lip_row',
              command=(py.Callback(show_group, 'up_lip_locator_grp')))
    u_lip_menu = py.popupMenu('u_lip_menu', p=u_lip_btn, ctl=False, button=3)
    py.menuItem('Reset Locators', p=u_lip_menu, command=py.Callback(reset_locators, 'up_lip_locator_grp'))
    py.button('u_guide_btn', label='Guide', p='u_lip_row', command=py.Callback(guide_gui, 'upmouth.png', full=True))

    py.rowLayout('l_lip_row', p='master_column', numberOfColumns=3)
    l_lip_btn = py.button('l_lip_btn', label='Place Lower Lip Locators', w=button_width,  p='l_lip_row',
              command=(py.Callback(show_group, 'low_lip_locator_grp')))
    l_lip_menu = py.popupMenu('l_lip_menu', p=l_lip_btn, ctl=False, button=3)
    py.menuItem('Reset Locators', p=l_lip_menu, command=py.Callback(reset_locators, 'low_lip_locator_grp'))
    py.button('l_guide_button', label='Guide', p='l_lip_row', command=py.Callback(guide_gui, 'lowmouth.png', full=True))

    py.rowLayout('slider_row', p='master_column', numberOfColumns=3)
    py.text('Locator Scale   ', p='slider_row')
    py.floatSlider('locator_scale', min=.5, max=50, value=1, step=1, p='slider_row')

    py.frameLayout('image_frame', label='Guide Preview', p='master_row')
    py.image("guide", p='image_frame', w=150, h=150, dgc=(py.Callback(guide_gui, 'open')))

    py.rowColumnLayout('final_row', p='god_column')
    py.button('show_all_button', label='Show All', p='final_row', width=window_size[0]-5,
              command=py.Callback(show_group, 'all'))
    py.button('confirm_button', label='Confirm', p='final_row', width=window_size[0]-5,
              command=py.Callback(joint_creation))
    con.connect_locators()
    py.showWindow(window)


def guide_gui(filename, **kwargs):
    size_bool = kwargs.setdefault('full', False)
    if size_bool is True:
        image_path = get_file_path('images/'+filename)
        window = 'guide_gui'
        window_title = 'Guide'
        window_size = (450, 472)
        if py.window(window, exists=True):
            py.deleteUI(window, window=True)
        window_obj = py.window(window, title=window_title, widthHeight=window_size, sizeable=False)

        py.frameLayout('full_frame', label='Full Resolution Guide', p=window)
        py.image("full_guide", p='full_frame', w=450, h=472, i=image_path)
        py.showWindow(window)

    else:
        image_path = get_file_path('images/'+filename)
        py.image("guide", e=True, w=150, h=150, i=image_path)

def offset_gui(**kwargs):
    window = 'offset_gui'
    window_title = 'ecFaceSetup'
    window_size = (337, 245)
    if py.window(window, exists=True):
        py.deleteUI(window, window=True)
    if py.window('guide_gui', exists=True):
        py.deleteUI('guide_gui', window=True)
    if py.window('locator_placement_prompt', exists=True):
        py.deleteUI('locator_placement_prompt', window=True)
    window_obj = py.window(window, title=window_title, widthHeight=window_size, sizeable=False)
    py.frameLayout('offset_scale_frame', label='Scale Offset Controls', p=window)
    py.floatSlider('offset_scale', p='offset_scale_frame', min=1, max=20, value=1, step=1)
    py.rowLayout('offset_row', p=window, numberOfColumns=3)
    py.button('accept_button', label="Accept Configuration", p='offset_row', command=py.Callback(finalize))
    py.button('back_button', label="Back to Placement", p='offset_row',
              command=py.Callback(make_offset_groups, delete=True))
    con.connect_offset()
    py.showWindow(window)


def joint_creation():
    for key in sorted(cl.EcGroup.loc_name_pos_dict):
        joint_inst = cl.EcJoint()
        joint_inst.create_joints(key)
        joint_inst.set_parent(key)
    make_offset_groups()


def reset_locators(group_name):
    if group_name == 'all':
        for key in cl.EcGroup.group_children_dict:
            for i in range(len(cl.EcGroup.group_children_dict[key][0])):
                cl.EcGroup.group_children_dict[key][0][i][0].reset_position()
    else:
        for i in range(len(cl.EcGroup.group_children_dict[group_name][0])):
            cl.EcGroup.group_children_dict[group_name][0][i][0].reset_position()


def mirror_locators(**kwargs):
    file_name = kwargs.setdefault('filename')
    unmirror = kwargs.setdefault('unmirror', False)
    file_list = ['up_eye', 'low_eye', 'cheek', 'up_mouth', 'low_mouth']
    if unmirror is False:
        if file_name == 'all':
            for i in range(0, len(file_list)):
                file_path = get_file_path('expressions/%s' % file_list[i])
                with open(file_path) as myfile:
                    expressionData = myfile.read()
                mc.expression(string=expressionData, name="%s_Expression" % file_list[i], ae=1, uc='all')
            py.headsUpMessage('Mirroring for all enabled. Must unmirror to reset locations')
        else:
            file_path = get_file_path('expressions/%s' % file_name)
            with open(file_path) as myfile:
                expressionData = myfile.read()
            mc.expression(string=expressionData, name="%s_Expression" % file_name, ae=1, uc='all')
            py.headsUpMessage('Mirroring for %s enabled. Must unmirror to reset locations' % file_name)
    else:
        for i in range(0, len(file_list)):
            try:
                mc.delete('%s_Expression' % file_list[i])
            except:
                pass
        py.headsUpMessage('Mirroring disabled')


def make_offset_groups(**kwargs):
    py.showHidden('baseoffset')
    py.hide('master_locator_grp')
    delete_bool = kwargs.setdefault('delete', False)
    if delete_bool is True:
        for key in cl.EcGroup.group_offset_dict:
            for i in range(0, len(cl.EcGroup.group_offset_dict[key])):
                try:
                    print 'deleting %s' % key
                    py.delete(cl.EcGroup.group_offset_dict[key][i].group_name)
                except:
                    print 'Tried to delete %s' % key
        py.delete('cn_head_jnt', 'low_jaw_grp')
        py.showHidden('master_locator_grp')
        py.hide('baseoffset')
        locator_placement_gui()
    else:
        master_jaw_grp = cl.EcGroup(groupName='low_jaw_grp').set_parent(operation='offset', parent='master_offset_grp')\
            .match(DriveObject='cn_head_low_jaw_jnt').match(DrivenObject='master_offset_grp', DriveObject='cn_head_jnt',
                                                            type='parent', maintainOffset=True)\
            .match(DrivenObject='follicles_grp', DriveObject='cn_head_jnt', type='parent', maintainOffset=True)
        for key in cl.EcGroup.loc_name_pos_dict:
            num = 2
            parent = 'master_offset_grp'
            side = ['rt_', 'lf_']
            if key == 'head_low_jaw' or key == 'head':
                main_offset = [None]
            elif key == 'mouth_center_up':
                main_offset = []
                main_offset.append(cl.EcGroup(groupName='cn_'+key+'_m_grp'))
                offset_group = cl.EcGroup(groupName='cn_'+key+'_offset_grp')
                main_offset[0].set_parent(operation='offset', parent=parent)\
                        .match(DriveObject='cn_'+key+'_jnt')
                offset_group.set_parent(operation='offset', parent=main_offset[0].group_name)\
                        .match(DriveObject='cn_'+key+'_jnt')\
                    .match(DriveObject='cn_'+key+'_f', deleteConstraint=False, maintainOffset=True)
                offset = cl.EcOffset(key, 'cn_', offset_group.group_name)
            elif 'mouth' in key:
                if 'low' in key:
                    if key == 'mouth_center_low':
                        side = ['cn_']
                        num = 1
                        parent = 'low_jaw_grp'
                    else:
                        parent = 'low_jaw_grp'
                main_offset = []
                for i in range(0, num):
                    main_offset.append(cl.EcGroup(groupName=side[i]+key+'_m_grp'))
                    offset_group = cl.EcGroup(groupName=side[i]+key+'_offset_grp')
                    main_offset[i].set_parent(operation='offset', parent=parent)\
                        .match(DriveObject=side[i]+key+'_jnt')
                    offset_group.set_parent(operation='offset', parent=main_offset[i].group_name)\
                        .match(DriveObject=side[i]+key+'_jnt')\
                        .match(DriveObject=side[i]+key+'_f', deleteConstraint=False, maintainOffset=True)
                    rotate_offset = cl.EcGroup(groupName=side[i]+key+'_rotate_grp')\
                        .set_parent(operation='offset', parent=offset_group.group_name)
                    if 'low' in key:
                        rotate_offset.match(DriveObject='cn_head_low_jaw_jnt', deleteConstraint=False, type='parent')
                    offset = cl.EcOffset(key, side[i], rotate_offset.group_name).freeze()
            else:
                main_offset = []
                for i in range(0, num):
                    main_offset.append(cl.EcGroup(groupName=side[i]+key+'_m_grp'))
                    offset_group = cl.EcGroup(groupName=side[i]+key+'_offset_grp')
                    main_offset[i].set_parent(operation='offset', parent=parent)\
                        .match(DriveObject=side[i]+key+'_jnt')
                    offset_group.set_parent(operation='offset', parent=main_offset[i].group_name)\
                        .match(DriveObject=side[i]+key+'_jnt')\
                    .match(DriveObject=side[i]+key+'_f', deleteConstraint=False, maintainOffset=True)
                    offset = cl.EcOffset(key, side[i], offset_group.group_name)
            cl.EcGroup.group_offset_dict[key] = main_offset
        py.hide('baseoffset')
        offset_gui()


def delete_locators():
    py.delete('Master_Grp', 'PhonemeController', 'baseoffset', 'master_locator_grp', 'master_offset_grp')
    py.deleteUI('locator_placement_prompt')


def finalize():
    py.delete('baseoffset', 'master_locator_grp')
    py.parent('master_offset_grp', 'Master_Grp')
    py.parentConstraint('cn_head_jnt', 'follicles_grp', mo=True)
    py.select('cn_head_jnt')
    py.deleteUI('offset_gui')
    mel_file = 'facialrig_Animation_GUI.mel'
    file_path = get_file_path(mel_file)
    py.mel.source(file_path.replace('\\', '/'))

