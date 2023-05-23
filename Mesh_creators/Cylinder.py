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


def mesh_pydata(radius: float, height: float, segments: int) -> Tuple[List[Tuple]]:
    print("Pydata Generated")
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, vertices=segments, location=(0, 0, 0))
    cylinder_obj = bpy.context.active_object
    mesh = cylinder_obj.data
    vertices = [(v.co.x, v.co.y, v.co.z) for v in mesh.vertices]
    edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]
    faces = [tuple(f.vertices) for f in mesh.polygons]
    bpy.data.objects.remove(cylinder_obj)
    pydata = vertices, edges, faces
    print(pydata)
    return pydata

def create_collection(collection_name: str) -> Collection:
    '''
    Создает новую коллекцию с указанным именем, если ее не существует,
    или возвращает существующую коллекцию с указанным именем.
    '''
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    else:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
        return collection


def create_obj():
    print("\nSTART")
    mesh_name = "TEST"
    col_name = "Test Pydata"
    col = create_collection(col_name)
    mesh = mesh_new(mesh_name)
    assert type(mesh) == Mesh
    obj = obj_new(mesh_name, mesh)
    assert type(obj) == Object
    ob_to_col(obj, col)
    radius = 2.0
    height = 4.0
    segments = 64
    pydata = mesh_pydata(radius, height, segments)
    mesh.from_pydata(vertices=pydata[0], edges=pydata[1], faces=pydata[2])
    print("Pydata Assigned")

if __name__ == "__main__":
    create_obj()
