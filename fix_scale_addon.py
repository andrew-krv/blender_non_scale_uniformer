bl_info = {
    "name": "Fix Non-Uniform Scale",
    "author" : "Andrii Kryvytskyi (GitHub:andrew-krv)",
    "version": (0, 1),
    "blender": (3, 3, 9),
    "description": "Addon that fixes non-uniform 1 scale to uniform 1",
    "warning" : "Usage may alter vertices location for negative scale and brake normals",
    "tracker_url" : "https://github.com/andrew-krv/blender_scale_uniformer/issues",
    "support" : "COMMUNITY",
    "location": "3DView -> Tool Shelf -> Non-Uniform Scale Fix",
    "category": "Object",
}

import bpy
from bpy.props import BoolProperty
from math import isclose

EPSILON = 1e-3

class OBJECT_OT_select_non_uniform_scale(bpy.types.Operator):
    bl_idname = "object.select_non_uniform_scale"
    bl_label = "Select Non-Uniform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            obj.select_set(False)
            if not all(isclose(s, 1.0, abs_tol=EPSILON) for s in obj.scale):
                obj.select_set(True)

        return {'FINISHED'}

class OBJECT_OT_fix_non_uniform_scale(bpy.types.Operator):
    bl_idname = "object.fix_non_uniform_scale"
    bl_label = "Fix Non-Uniform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    # Recursive function to correct scale
    def correct_scale(self, obj):
        # If the object's scale is (1, 1, 1), no correction is needed
        if obj.scale == (1.0, 1.0, 1.0):
            return

        correction_factor = (1 / obj.scale[0], 1 / obj.scale[1], 1 / obj.scale[2])

        # Apply the correction factor to the object's vertices if it's a mesh
        if obj.type == 'MESH':
            for vertex in obj.data.vertices:
                vertex.co.x /= correction_factor[0]
                vertex.co.y /= correction_factor[1]
                vertex.co.z /= correction_factor[2]

        # Reset the object's scale to (1, 1, 1)
        obj.scale = (1.0, 1.0, 1.0)

        # Apply the correction factor to child objects
        for child in obj.children:
            # Adjust the location of the child before the recursive call
            child.location.x /= correction_factor[0]
            child.location.y /= correction_factor[1]
            child.location.z /= correction_factor[2]

            child.scale.x /= correction_factor[0]
            child.scale.y /= correction_factor[1]
            child.scale.z /= correction_factor[2]

            # If the child has animation data, modify the location keyframes
            if child.animation_data and child.animation_data.action:
                for fcurve in child.animation_data.action.fcurves:
                    if fcurve.data_path.endswith('location'):
                        for keyframe_point in fcurve.keyframe_points:
                            keyframe_point.co[1] /= correction_factor[fcurve.array_index]

            # Recursively apply corrections to children
            self.correct_scale(child)


    def execute(self, context):
        objects = bpy.context.selected_objects if context.scene.only_selected else bpy.data.objects

        for obj in objects:
            self.correct_scale(obj)

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
        row.operator("object.fix_non_uniform_scale")

        row = layout.row()
        row.prop(context.scene, "only_selected")

def register():
    bpy.utils.register_class(OBJECT_OT_select_non_uniform_scale)
    bpy.utils.register_class(OBJECT_OT_fix_non_uniform_scale)
    bpy.utils.register_class(OBJECT_PT_non_uniform_scale)
    bpy.types.Scene.only_selected = BoolProperty(
        name="Selected Only",
        description="Apply fix to selected objects only",
        default=True
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_non_uniform_scale)
    bpy.utils.unregister_class(OBJECT_OT_fix_non_uniform_scale)
    bpy.utils.unregister_class(OBJECT_PT_non_uniform_scale)
    del bpy.types.Scene.only_selected

if __name__ == "__main__":
    register()
