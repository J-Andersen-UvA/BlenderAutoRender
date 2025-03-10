import bpy

def get_armature_from_collection(collection_name):
    return next(obj for obj in bpy.data.collections[collection_name].objects if obj.type == 'ARMATURE')

def copy_bone_rolls():
    # If two armatures are selected, copy bone rolls from the active armature to the other, otherwise
    # use mainAvatar and importedAnimation collections to find these armatures.
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']

    if len(selected_objects) == 2:
        print("Using selected armatures...")
        source_armature = bpy.context.object  # Active object
        target_armature = next(obj for obj in selected_objects if obj != source_armature)
    else:
        print("Getting armatures from collections...")
        source_armature = get_armature_from_collection("importedAnimation")
        target_armature = get_armature_from_collection("mainAvatar")
        if source_armature is None or target_armature is None:
            print("Please select exactly two armatures or ensure mainAvatar and importedAnimation collections exist.")
            return
    
    print(f"\nCopying bone rolls from {source_armature.name} to {target_armature.name}\n")

    # Ensure source and target are in Edit Mode
    bpy.context.view_layer.objects.active = source_armature
    bpy.ops.object.mode_set(mode='EDIT')
    source_bones = {bone.name: bone.roll for bone in source_armature.data.edit_bones}

    bpy.context.view_layer.objects.active = target_armature
    bpy.ops.object.mode_set(mode='EDIT')
    target_bones = target_armature.data.edit_bones

    edited = False
    for bone_name, source_roll in source_bones.items():
        if bone_name in target_bones:
            target_bones[bone_name].roll = source_roll
            edited = True

    # Return to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    if not edited:
        print("No bone rolls copied.")
    else:
        print("Bone rolls copied successfully.")

