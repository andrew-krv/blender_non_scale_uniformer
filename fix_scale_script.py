import bpy

# Ensure we are in Object Mode
bpy.ops.object.mode_set(mode='OBJECT')

# Recursive function to correct scale
def correct_scale(obj):
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
        correct_scale(child)

# Iterate over all objects in the Blender file
for obj in bpy.data.objects:
    correct_scale(obj)

# Ensure we end in Object Mode
bpy.ops.object.mode_set(mode='OBJECT')
