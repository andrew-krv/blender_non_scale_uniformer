bl_info = {
    "name": "Fix Non-Uniform Scale",
    "author" : "Andrii Kryvytskyi (GitHub:andrew-krv)",
    "version": (0, 2),
    "blender": (3, 3, 9),
    "description": "Addon that fixes non-uniform 1 scale to uniform 1",
    "warning" : "Usage may brake normals for negative scale objects. Fix them using \"Flip normals\" button or manually.",
    "tracker_url" : "https://github.com/andrew-krv/blender_scale_uniformer/issues",
    "support" : "COMMUNITY",
    "location": "3DView -> Tool Shelf -> Non-Uniform Scale Fix",
    "category": "Object",
}

import bpy
from . import fix_scale
from bpy.props import BoolProperty
from math import isclose


class OBJECT_OT_select_non_uniform_scale(bpy.types.Operator):
    bl_idname = "object.select_non_uniform_scale"
    bl_label = "Select Non-Uniform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        fix_scale.select_invalid_scale()

        return {'FINISHED'}

class OBJECT_OT_fix_non_uniform_scale(bpy.types.Operator):
    bl_idname = "object.fix_non_uniform_scale"
    bl_label = "Fix Non-Uniform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects = bpy.context.selected_objects if context.scene.only_selected else bpy.data.objects

        for obj in objects:
            fix_scale.correct_scale(obj)

        return {'FINISHED'}

class OBJECT_OT_flip_selected_normals(bpy.types.Operator):
    bl_idname = "object.flip_selected_normals"
    bl_label = "Flip normals (Selected)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Make a copy of the selected objects list
        selected_objects = list(bpy.context.selected_objects)

        # Iterate over the copied list
        for obj in selected_objects:
            if obj.type == 'MESH':
                fix_scale.flip_normals(obj)

        return {'FINISHED'}

class OBJECT_PT_non_uniform_scale(bpy.types.Panel):
    bl_label = "Non-Uniform Scale Fix"
    bl_idname = "OBJECT_PT_non_uniform_scale"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.select_non_uniform_scale")

        row = layout.row()
        row.operator("object.flip_selected_normals")

        row = layout.row()
        row.operator("object.fix_non_uniform_scale")

        row = layout.row()
        row.prop(context.scene, "only_selected")

def register():
    bpy.utils.register_class(OBJECT_OT_select_non_uniform_scale)
    bpy.utils.register_class(OBJECT_OT_fix_non_uniform_scale)
    bpy.utils.register_class(OBJECT_OT_flip_selected_normals)
    bpy.utils.register_class(OBJECT_PT_non_uniform_scale)
    bpy.types.Scene.only_selected = BoolProperty(
        name="Selected Only",
        description="Apply fix to selected objects only",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_non_uniform_scale)
    bpy.utils.unregister_class(OBJECT_OT_fix_non_uniform_scale)
    bpy.utils.unregister_class(OBJECT_OT_flip_selected_normals)
    bpy.utils.unregister_class(OBJECT_PT_non_uniform_scale)
    del bpy.types.Scene.only_selected

if __name__ == "__main__":
    register()
