bl_info = {
    "name": "ShapeKeysChecker",
    "author": "takec",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "",
    "description": "Baseに対して変更されている頂点を選択",
    "category": "Object"
}

if "bpy" in locals():
    import imp
    imp.reload(shape_keys_checker)
else:
    from . import shape_keys_checker

import bpy

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(shape_keys_checker.ShapeKeysChecker.bl_idname)

classes = [
    shape_keys_checker.ShapeKeysChecker,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()