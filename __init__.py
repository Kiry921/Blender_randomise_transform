# Мини-аддон, который рандомизирует scale объектов сцены (здесь на примере созданной ранее плоскости)

'''    
Для выбранного в данный момент объекта нужны кнопки:
    - выбор, меняется ли размер по всем осям одинаково или по каждой отдельно (bool)
    - выбор рамок, в которых будет рандомно изменяться объект:
        3 значения Float (для X, Y, Z) для минимальных значений рандома
        3 значения Float (для X, Y, Z) для максимальных значений рандома
    - кнопка оператора
'''

#Для того, чтобы сделать из скрипта аддон:    
bl_info = {
    "name": "Blender_randomize_scale",
    "author": "Klimov Kirill",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View 3D -> UI -> Randomise",
    "description": "Randomise scale of selected objects",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
from typing import List
from random import randint
from bpy.types import Operator, Panel, PropertyGroup, Object
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty, FloatProperty, PointerProperty


class RandomizeProps(PropertyGroup):
    change_even: BoolProperty(
        name='Change Even',
        default=True
    )
    minx: FloatProperty(
        name='Min X',
        default=.2,
        soft_min=0,
        soft_max=2,
        subtype='FACTOR'
    )
    maxx: FloatProperty(
        name='Max X',
        default=2,
        soft_min=0,
        soft_max=2,
        subtype='FACTOR'
    )
    miny: FloatProperty(
        name='Min Y',
        default=.2,
        soft_min=0,
        soft_max=2,
        subtype='FACTOR'
    )
    maxy: FloatProperty(
        name='Max Y',
        default=2,
        soft_min=0,
        soft_max=2,
        subtype='FACTOR'
    )
    minz: FloatProperty(
        name='Min Z',
        default=.2,
        soft_min=0,
        soft_max=2,
        subtype='FACTOR'
    )
    maxz: FloatProperty(
        name='Max Z',
        default=2,
        soft_min=0,
        soft_max=2,
        subtype='FACTOR'
    )


class RandomizeScale(Operator):
    bl_idname = 'object.random_scale'
    bl_label = 'Randomize Scale'
    change_even = None
    minx = None
    maxx = None
    miny = None
    maxy = None
    minz = None
    maxz = None

    def structure(self, context):
        props = context.scene.rand
        self.change_even = props.change_even
        self.minx = props.minx
        self.maxx = props.maxx
        self.miny = props.miny
        self.maxy = props.maxy
        self.minz = props.minz
        self.maxz = props.maxz
        self.scene = context.scene

    def get_random(self, min: float, max: float) -> float:
        return randint(int(min * 100), int(max * 100)) / 100

    def get_selected_objects(self) -> List[Object]:
        return [ob for ob in self.scene.objects if ob.select_get()]

    def randomize(self):
        objects = self.get_selected_objects()
        for ob in objects:
            sc_x = self.get_random(self.minx, self.maxx)
            if self.change_even:
                ob.scale = (sc_x, sc_x, sc_x)
            else:
                sc_y = self.get_random(self.miny, self.maxy)
                sc_z = self.get_random(self.minz, self.maxz)
                ob.scale = (sc_x, sc_y, sc_z)

    def execute(self, context) -> set:
        self.structure(context)
        self.randomize()
        return {'FINISHED'}


class OBJECT_PT_RandomizeScalePanel(Panel):
    bl_label = "Randomize Scale"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Randomize'

    def draw(self, context):
        layout = self.layout
        props = context.scene.rand  # Создали временные переменные

        col = layout.column()  # Создали колонку для Change even
        col.prop(props, "change_even")

        col = layout.column()  # Создали колонку и коробочку для min и max X,Y,Z
        box = col.box()
        spl = box.split(align=True)
        spl.prop(props, "minx")
        spl.prop(props, "maxx")
        spl = box.split(align=True)
        spl.enabled = not props.change_even
        spl.prop(props, "miny")
        spl.prop(props, "maxy")
        spl = box.split(align=True)
        spl.enabled = not props.change_even
        spl.prop(props, "minz")
        spl.prop(props, "maxz")

        row = layout.row()  # Ряд для оператора
        row.operator('object.random_scale')


classes = [
    RandomizeProps,
    RandomizeScale,
    OBJECT_PT_RandomizeScalePanel
]


def register():
    for cl in classes:
        register_class(cl)
    bpy.types.Scene.rand = PointerProperty(type=RandomizeProps)


def unregister():
    for cl in reversed(classes):
        unregister_class(cl)


if __name__ == '__main__':
