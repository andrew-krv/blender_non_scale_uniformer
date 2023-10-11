import bpy
from math import isclose

EPSILON = 1e-3

def select_invalid_scale():
    for obj in bpy.data.objects:
        obj.select_set(False)
        if not all(isclose(s, 1.0, abs_tol=EPSILON) for s in obj.scale):
            if obj.name in [o.name for o in bpy.context.view_layer.objects]:
                obj.select_set(True)
        else:
            print(f"Object {obj.name} is not in the current view layer.")

def flip_normals(obj):
    if obj.name in [o.name for o in bpy.context.view_layer.objects]:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print(f"Object {obj.name} is not in the current view layer.")


# Recursive function to correct scale
def correct_scale(obj):
    # If the object's scale is (1, 1, 1), no correction is needed
    if all(isclose(s, 1.0, abs_tol=EPSILON) for s in obj.scale):
        return

    correction_factor = (1 / obj.scale[0], 1 / obj.scale[1], 1 / obj.scale[2])

    # Apply the correction factor to the object's vertices if it's a mesh
    if obj.type == 'MESH':
        for vertex in obj.data.vertices:
            vertex.co.x /= correction_factor[0]
            vertex.co.y /= correction_factor[1]
            vertex.co.z /= correction_factor[2]

        if obj.scale.x < 0 or obj.scale.y < 0 or obj.scale.z < 0:
            flip_normals(obj)

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
        correct_scale(child)
