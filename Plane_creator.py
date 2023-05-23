# Создание объекта, сделано для плоскости
import bpy
from bpy.types import Mesh, Object, Collection
from typing import Tuple, List


def mesh_new(name: str) -> Mesh:
    '''
    Проверяет, есть ли имя в списке существующих мешей,
    если есть - использует меш с этим именем, обнулив ему геометрию
    если нет - создает новый пустой меш с этим именем
    возвращает меш
    '''
    print("Mesh created")
    if name in bpy.data.meshes:
        mesh = bpy.data.meshes[name]
        mesh.clear_geometry()
    else:
        mesh = bpy.data.meshes.new(name)
    print(mesh)
    return mesh


def obj_new(obj_name: str, mesh: Mesh) -> Object:
    '''
    Проверяет, есть ли имя в списке существующих объектов,
    если есть - привязывает меш в качестве данных объекта
    если нет - создает новый объект с этим именем и с мешем в качестве данных
    возвращает объект
    '''
    print("Object created")
    if obj_name in bpy.data.objects:
        obj = bpy.data.objects[obj_name]
        assert obj.type == 'MESH'
        obj.data = mesh
    else:
        obj = bpy.data.objects.new(obj_name, mesh)
    print(obj)
    return obj


def ob_to_col(obj: Object, col: Collection) -> None:
    '''
    Отвязывает объект от всех коллекций и от всех мастер-коллекций в сценах
    Привязывает к нужной нам коллекции
    '''
    print("Object linked to Collection")
    for c in bpy.data.collections:
        if obj.name in c.objects:
            c.objects.unlink(obj)
    for sc in bpy.data.scenes:
        if obj.name in sc.collection.objects:
            sc.collection.objects.unlink(obj)
    col.objects.link(obj)


def mesh_pydata() -> Tuple[List[Tuple]]:
    '''
    ( [(),(),(),()...],[]... [] )
    возвращает:
        - координаты каждого вертекса в виде списка кортежей
        - пары индексов вертексов для каждого эджа, либо пустой список
        - список кортежей, содержащих индексы вертексов каждого фейса
    '''

    print("Pydata Generated")
    vertices = [
        (-1, -1, 0),  # index 0
        (-1, 1, 0),  # index 1
        (1, 1, 0),  # index 2
        (1, -1, 0)  # index 3
    ]
    edges = []
    faces = [
        (0, 1, 2, 3)
    ]
    for i, f in enumerate(faces):
        faces[i] = tuple(reversed(f))

    pydata = vertices, edges, faces
    print(pydata)
    return pydata


def create_obj():
    print("\nSTART")
    mesh_name = "TEST"
    col_name = "Test Pydata"
    assert col_name in bpy.data.collections
    col = bpy.data.collections[col_name]
    mesh = mesh_new(mesh_name)
    assert type(mesh) == Mesh
    obj = obj_new(mesh_name, mesh)
    assert type(obj) == Object
    ob_to_col(obj, col)
    pydata = mesh_pydata()
    mesh.from_pydata(vertices=pydata[0], edges=pydata[1], faces=pydata[2])
    print("Pydata Assigned")


if __name__ == "__main__":
    create_obj()
