bl_info = {
    "name": "Armature Cleanup",
    "blender": (2, 81, 0),
    "category": "Rigging"
}

import bpy

class CleanupBones(bpy.types.Operator):
    """Cleans up an Armature by recalculating each bones tail position"""
    bl_idname = "bpy.ops"
    bl_label = "Cleanup Bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        armature_obj = context.active_object
        if armature_obj.type != "ARMATURE":
            self.report('ERROR_INVALID_INPUT', 'Selected object need to be an Armature')
            return {'FINISHED'}
        bpy.ops.object.mode_set(mode="EDIT")
        no_children_bones = []
        for bone in armature_obj.data.edit_bones:
            child_bone_sum = [0, 0, 0]
            child_count = 0
            for child in bone.children:
                child_bone_sum = [a+b for a, b in zip(child_bone_sum, child.head)]
                child_count += 1
            if child_count == 0:
                if bone.parent is not None:
                    no_children_bones.append(bone)
            else:
                for i in range(0, 3):
                    bone.tail[i] = child_bone_sum[i]/child_count
        for bone in no_children_bones:
            disp = [0, 0, 0]
            for i in range(0, 3):
                disp[i] = bone.parent.tail[i] - bone.parent.head[i]
            bone.tail = [a+b for a, b in zip(bone.head, disp)]
        bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CleanupBones)

def unregister():
    bpy.utils.unregister_class(CleanupBones)

if __name__ == "__main__":
    register()