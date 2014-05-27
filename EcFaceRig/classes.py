import pymel.core as py


class EcGroup(object):
    loc_name_pos_dict = {"head": (0, 0.328, -2),
                                  "head_low_jaw": (0, -0.343, -1.5),
                                  "up_eye_inner": (-0.371, 1.236, 0.697),
                                  "up_eye_mid": (-0.963, 1.413, 0.599),
                                  "up_eye_outer": (-1.296, 1.418, 0.421),
                                  "low_eye_inner": (-0.636, 0.519, 0.32),
                                  "low_eye_mid": (-1.003, 0.485, 0.169),
                                  "low_eye_outer": (-1.653, 0.226, -0.31),
                                  "upper_cheek": (-0.914, -0.051, 0.51),
                                  "outer_cheek": (-1.512, -0.889, -0.292),
                                  "nose": (-0.578, -0.25, 0.649),
                                  "low_cheek": (-0.937, -1.026, 0.422),
                                  "mouth_outer": (-.743, -0.927, 0.463),
                                  "mouth_up_outermid": (-.507, -0.776, 0.991),
                                  "mouth_up_innermid": (-.232, -0.739, 1.185),
                                  "mouth_low_outermid": (-0.562, -1.061, 0.856),
                                  "mouth_low_innermid": (-0.227, -1.112, 1.058),
                                  "mouth_center_low": (0, -1.125, 1.124),
                                  "mouth_center_up": (0, -0.755, 1.262)}
    group_children_dict = {}
    group_offset_dict = {}

    def __init__(self, **kwargs):
        self.group_name = kwargs.setdefault('groupName')
        self.number_of_children = kwargs.setdefault('numberOfChildren')
        self.children = []
        self.parent = ''
        self.group = py.group(name=self.group_name, empty=True)

    def toggle_visibility(self):
        if py.getAttr(self.group_name+'.v') is True:
            py.setAttr(self.group_name+'.v', False)
            print('Set %s visibility to False' % self.group_name)
        else:
            py.setAttr(self.group_name+'.v', True)
        return self.group_name

    def set_children(self):
        EcGroup.group_children_dict[self.group_name] = []
        for i in range(0, self.number_of_children):
            for k in range(0, len(self.children[i][1])):
                py.parent(self.children[i][1][k], self.group_name)
        EcGroup.group_children_dict[self.group_name].append(self.children)
        return self.group_name

    def set_parent(self, **kwargs):
        operation = kwargs.setdefault('operation', 'locator')
        child = kwargs.setdefault('child', self.group_name)
        parent = kwargs.setdefault('parent', self.group_name)
        if operation == 'locator':
            if self.group_name == 'master_locator_grp' or self.group_name == 'master_offset_grp':
                pass
            else:
                print 'parenting %s to master_locator_grp' % self.group
                py.parent(self.group, 'master_locator_grp')
        elif operation == 'offset':
            py.parent(child, parent)
        else:
            print 'Parenting has broken'
        return self


    def create_locators(self):
        if self.group_name == 'up_eye_locator_grp':
            for key in self.loc_name_pos_dict:
                if 'up_eye' in key:
                    locator_instance = EcLocator()
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, False))
                    locator_instance.move_to_position()
            self.number_of_children = 3
            self.set_children()

        elif self.group_name == 'low_eye_locator_grp':
            for key in self.loc_name_pos_dict:
                if 'low_eye' in key:
                    locator_instance = EcLocator()
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, False))
                    locator_instance.move_to_position()
            self.number_of_children = 3
            self.set_children()

        elif self.group_name == 'cheek_locator_grp':
            for key in self.loc_name_pos_dict:
                if 'cheek' in key or 'nose' in key:
                    locator_instance = EcLocator()
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, False))
                    locator_instance.move_to_position()
            self.number_of_children = 4
            self.set_children()

        elif self.group_name == 'up_lip_locator_grp':
            for key in self.loc_name_pos_dict:
                locator_instance = EcLocator()
                if 'mouth_up' in key:
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, False))
                    locator_instance.move_to_position()
                if 'center_up' in key:
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, True))
                    locator_instance.move_to_position()
                if 'mouth_outer' in key:
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, False))
                    locator_instance.move_to_position()
            self.number_of_children = 4
            self.set_children()

        elif self.group_name == 'low_lip_locator_grp':
            for key in self.loc_name_pos_dict:
                if 'mouth_low' in key:
                    locator_instance = EcLocator()
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, False))
                    locator_instance.move_to_position()
                if 'center_low' in key:
                    locator_instance = EcLocator()
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, True))
                    locator_instance.move_to_position()
            self.number_of_children = 3
            self.set_children()

        elif self.group_name == 'head_locator_grp':
            for key in self.loc_name_pos_dict:
                if 'head' in key:
                    locator_instance = EcLocator()
                    self.children.append(locator_instance.create_locators(self.loc_name_pos_dict[key], key, True))
                    locator_instance.move_to_position()
            self.number_of_children = 2
            self.set_children()
        else:
            print '%s does not need locators' % self.group_name

    def match(self, **kwargs):
        object = kwargs.setdefault('DrivenObject', self.group_name)
        destination = kwargs.setdefault('DriveObject', self.group_name)
        offset_bool = kwargs.setdefault('maintainOffset', False)
        delete_bool = kwargs.setdefault('deleteConstraint', True)
        constraint_type = kwargs.setdefault('type', 'point')
        if constraint_type == 'point':
            constraint = py.pointConstraint(destination, object, mo=offset_bool)
        elif constraint_type == 'parent':
            constraint = py.parentConstraint(destination, object, mo=offset_bool)
        if delete_bool is True:
            py.delete(constraint)
        py.select(cl=True)
        return self



class EcLocator(object):
    def __init__(self):
        self.locator_name = ''
        self.locator = []
        self.original_positions = []
        self.new_position = [(0, 0, 0), (0, 0, 0)]
        self.grp_position = []

    def create_locators(self, position, key, centered):
        self.locator_name = key
        if centered is True:
            self.locator.append(py.spaceLocator(n='cn_' + self.locator_name + '_L'))
            py.setAttr((self.locator[0] + "Shape.localScaleX"), .05)
            py.setAttr((self.locator[0] + "Shape.localScaleY"), .05)
            py.setAttr((self.locator[0] + "Shape.localScaleZ"), .05)
            py.connectAttr((self.locator[0] + ".scaleX"), (self.locator[0] + ".scaleY"))
            py.connectAttr((self.locator[0] + ".scaleX"), (self.locator[0] + ".scaleZ"))
            self.original_positions.append(position)
        else:
            self.locator = [py.spaceLocator(n='rt_' + self.locator_name + '_L'),
                            py.spaceLocator(n='lf_' + self.locator_name + '_L')]
            for i in range(0, 2):
                py.setAttr((self.locator[i] + "Shape.localScaleX"), .05)
                py.setAttr((self.locator[i] + "Shape.localScaleY"), .05)
                py.setAttr((self.locator[i] + "Shape.localScaleZ"), .05)
                py.connectAttr((self.locator[i] + ".scaleX"), (self.locator[i] + ".scaleY"))
                py.connectAttr((self.locator[i] + ".scaleX"), (self.locator[i] + ".scaleZ"))
            left_position = (position[0]*-1, position[1], position[2])
            self.original_positions = [position, left_position]
        locator_objects = [self, self.locator]
        return locator_objects

    def get_name(self):
        return self.locator

    def set_name(self, **kwargs):
        #currently doesnt account for two locators
        new_name = kwargs.setdefault('newName')
        py.rename(self.locator_name, new_name)
        return self.locator

    def move_to_position(self):
        for i in range(0, len(self.locator)):
            py.select(self.locator[i])
            py.move(self.original_positions[i])
            self.grp_position.append([py.getAttr(self.locator[i]+'.t')])
            print 'moving %s' % self.locator[i]
        return self.locator

    def reset_position(self):
        for i in range(0, len(self.locator)):
            py.setAttr(self.locator[i]+'.t', (self.grp_position[i][0][0],
                                                 self.grp_position[i][0][1],
                                                 self.grp_position[i][0][2]))
        return self.locator

    def connect_to(self, connection):
        for i in range(0, len(self.locator)):
            py.connectControl(connection, self.locator[0]+'.scale', self.locator[1]+'.scale')



class EcJoint(object):
    def __init__(self):
        self.joint_name = ''
        self.joint = {}
        self.original_positions = []

    def create_joints(self, key):
        py.select(cl=True)
        if 'mouth_center' in key:
            self.joint[key] = [py.joint(n='cn_'+key+'_jnt', position=(py.xform('cn_'+key+'_L', q=True, t=True, a=True, ws=True)))]
        elif 'head' in key:
            self.joint[key] = [py.joint(n='cn_'+key+'_jnt', position=(py.xform('cn_'+key+'_L', q=True, t=True, a=True, ws=True)))]
        else:
            self.joint[key] = [py.joint(n='rt_'+key+'_jnt', position=(py.xform('rt_'+key+'_L', q=True, t=True, a=True, ws=True))),
                          py.joint(n='lf_'+key+'_jnt', position=(py.xform('lf_'+key+'_L', q=True, t=True, a=True, ws=True)))]
        py.select(cl=True)

    def set_parent(self, key):
        try:
            for i in range(0, len(self.joint[key])):
                if key == 'head':
                    pass
                elif key == 'head_low_jaw':
                    py.parent(self.joint[key][i], 'cn_head_jnt')
                elif 'mouth' in key:
                    if 'center_low' in key:
                        py.parent(self.joint[key][i], 'cn_head_low_jaw_jnt')
                    elif 'low' in key:
                        py.parent(self.joint[key][i], 'cn_head_low_jaw_jnt')
                    else:
                        py.parent(self.joint[key][i], 'cn_head_jnt')
                else:
                    py.parent(self.joint[key][i], 'cn_head_jnt')
        except IndexError:
            print 'Index Error: %s' % key


class EcOffset(object):
    def __init__(self, key, side, offset_group):
        self.offset_name = side+key+'_offset'
        self.offset_group = offset_group
        self.joint = side+key+'_jnt'
        self.offset = py.duplicate("baseoffset", n=self.offset_name)
        self.match(DrivenObject=self.offset_name, DriveObject=self.joint)
        py.parent(self.offset_name, self.offset_group)
        self.match(DriveObject=self.offset_name, DrivenObject=self.joint, deleteConstraint=False)
        py.connectAttr((self.offset_name + ".scaleX"), (self.offset_name + ".scaleY"))
        py.connectAttr((self.offset_name + ".scaleX"), (self.offset_name + ".scaleZ"))

    def match(self, **kwargs):
        object = kwargs.setdefault('DrivenObject', self.offset_name)
        destination = kwargs.setdefault('DriveObject', self.offset_name)
        offset_bool = kwargs.setdefault('maintainOffset', False)
        delete_bool = kwargs.setdefault('deleteConstraint', True)
        constraint_type = kwargs.setdefault('type', 'point')
        if constraint_type == 'point':
            constraint = py.pointConstraint(destination, object, mo=offset_bool)
        elif constraint_type == 'parent':
            constraint = py.parentConstraint(destination, object, mo=offset_bool)
        if delete_bool is True:
            py.delete(constraint)
        py.select(cl=True)
        return self

    def freeze(self):
        py.select(self.offset_name)
        py.makeIdentity(apply=True, t=1, r=1, n=0)
        py.select(clear=True)