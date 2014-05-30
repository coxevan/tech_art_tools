import pymel.core as py
from pymel.core.uitypes import IntSliderGrp


class DuplicateOnCurve(object):
    def __init__(self, **kwargs):
        self.frame_count = kwargs.setdefault('numberOfDuplicates')
        self.int_slider = ''
        self.objects = []
        self.parent_check = ''
        self.parent_bool = False
        self.motion_path = ''
        self.dup_obj = kwargs.setdefault('objToDuplicate')
        self.curve_obj = kwargs.setdefault('curve')
        gui_bool = kwargs.setdefault('gui', False)
        if gui_bool is True:
            self.create_gui()
        else:
            self.create_first_set()

    def create_gui(self):
        self.create_first_set()
        window = 'creation_gui'
        window_title = 'Duplicate Along Curve'
        window_size = (337, 245)
        if py.window(window, exists=True):
            py.deleteUI(window, window=True)
        window_obj = py.window(window, title=window_title, widthHeight=window_size, sizeable=False)
        gui_frame = py.frameLayout('duplicate_along_curve',
                                   label='Edit Parameters', p=window)
        self.int_slider = IntSliderGrp(label='Number of Duplicates',
                                       field=True,
                                       minValue=2, maxValue=20,
                                       fieldMinValue=2, fieldMaxValue=100,
                                       value=3,
                                       dc=py.Callback(self.iterative_creation),
                                       cc=py.Callback(self.iterative_creation))
        self.parent_check = py.checkBoxGrp(label='Parent Objects', cc=py.Callback(self.iterative_creation))
        window_obj.show()

    def create_first_set(self):
        self.motion_path = py.pathAnimation(self.dup_obj, self.curve_obj, stu=1, etu=self.frame_count)
        py.keyTangent(self.motion_path+'_uValue', index=(0, 1), inTangentType='linear')
        py.keyTangent(self.motion_path+'_uValue', index=(0, 1), outTangentType='linear')
        self.creation_loop()

    def iterative_creation(self):
        try:
            for obj in self.objects:
                py.delete(obj)
        except:
            pass
        self.frame_count = self.int_slider.getValue()
        self.parent_bool = self.parent_check.getValue1()
        self.motion_path = py.pathAnimation(self.dup_obj, self.curve_obj, stu=1, etu=self.frame_count)
        self.objects = []
        py.keyTangent(self.motion_path+'_uValue', index=(0, 1), inTangentType='linear')
        py.keyTangent(self.motion_path+'_uValue', index=(0, 1), outTangentType='linear')
        print "frame count = " + str(self.frame_count)

        self.creation_loop()

    def creation_loop(self):
        count = 0
        for i in xrange(1, self.frame_count+1):
            py.currentTime(i)
            self.objects.append(py.duplicate(self.dup_obj))
            count += 1
        if self.parent_bool is True:
            for i in xrange(1, len(self.objects)):
                py.parent(self.objects[i], self.objects[i-1])
            print "made: " + str(count)
        py.delete(self.motion_path)
