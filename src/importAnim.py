bl_info = {
    "name": "GLB Importer and Animator",
    "blender": (3, 0, 0),
    "category": "Import-Export",
    "author": "Your Name",
    "version": (1, 1),
    "description": "A tool to import GLB files and transfer animations to target avatars",
    "location": "View3D > Sidebar > GLB Importer",
    "warning": "",
    "support": "COMMUNITY",
}

import bpy
import sys

class GLBImporter:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.collection_name = "importedAnimation"
        self.action_body = None
        self.action = None
        self.shape_key_action = None
        self.animation_range = None
        if filepath:
            self.import_glb()

    def import_glb(self):
        if not self.filepath:
            raise ValueError("No file path provided for GLB import")

        bpy.ops.import_scene.gltf(filepath=self.filepath, bone_heuristic='TEMPERANCE')
        self.add_to_collection()
        self.find_action_body()
        self.find_shape_key_animation()

    def add_to_collection(self):
        if self.collection_name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(self.collection_name)
            bpy.context.scene.collection.children.link(new_collection)
        else:
            new_collection = bpy.data.collections[self.collection_name]

        for obj in bpy.context.selected_objects:
            bpy.context.scene.collection.objects.unlink(obj)
            new_collection.objects.link(obj)

    def find_action_body(self):
        if self.collection_name in bpy.data.collections:
            collection = bpy.data.collections[self.collection_name]
            for obj in collection.objects:
                if obj.type == 'ARMATURE':
                    self.action_body = obj  # Store the armature
                    
                    # Check if it has animation data and an action
                    if obj.animation_data and obj.animation_data.action:
                        self.action = obj.animation_data.action
                    else:
                        self.action = None  # No action found
                        raise ValueError("No action found for the armature")

                    break  # Stop after finding the first armature

    def find_shape_key_animation(self):
        """Finds and stores the animation action for shape keys in the imported mesh."""
        if self.collection_name in bpy.data.collections:
            collection = bpy.data.collections[self.collection_name]

            for obj in collection.objects:
                if obj.type == 'MESH' and obj.data.shape_keys:  # Mesh must have shape keys
                    self.shape_key_action = obj.data.shape_keys.animation_data.action
    
    def remove_collection_and_contents(self):
        if self.collection_name in bpy.data.collections:
            collection = bpy.data.collections[self.collection_name]
            bpy.data.collections.remove(collection)

    # Using the action, find the start and end frames of the animation
    def get_animation_range(self):
        """Returns the start and end frames of an animation action."""
        if not self.action or not self.action.fcurves:
            print("No animation data found.")
            return None, None

        # Collect all keyframe points from all F-Curves
        keyframes = [kp.co.x for fc in self.action.fcurves for kp in fc.keyframe_points]

        if not keyframes:
            print("No keyframes found in action.")
            return None, None

        # Find the min and max keyframe values
        start_frame = int(min(keyframes))
        end_frame = int(max(keyframes))

        return start_frame, end_frame

class AnimationTransfer:
    def __init__(self, source_action, source_shape_key_action, target_avatar_collection):
        self.source_action = source_action
        self.source_shape_key_action = source_shape_key_action
        self.target_avatar_collection = target_avatar_collection

    def check_validity(self):
        validity = True

        if not self.source_shape_key_action.data.shape_keys:
            print(f"Source object '{self.source_shape_key_action.name}' has no shape key animation.")
            validity = False

        for obj in self.target_avatar_collection.objects:
            if obj.type == 'MESH' and obj.data.shape_keys:  # Mesh must have shape keys
                self.target_avatar = obj
                break
            else:
                print(f"Target collection '{self.target_avatar_collection.name}' has no mesh objects with shape keys.")
                validity = False

        if not self.source_action:
            print(f"Source object '{self.source_action.name}' has no animation data.")
            validity = False

        return validity

    def transfer_shape_key_animation(self):
        """Copies shape key animation from source_obj to target_obj while preserving F-Curves."""
        # Set target avatar shape keys to match source shape keys
        for obj in self.target_avatar_collection.objects:
            if obj.type == 'MESH' and obj.data.shape_keys:  # Mesh must have shape keys
                obj.data.shape_keys.animation_data.action = self.source_shape_key_action

    def transfer_bone_animation(self):
        """Copies bone animation from source_obj to target_obj while preserving F-Curves."""
        # Get target avatar armature
        for obj in self.target_avatar_collection.objects:
            if obj.type == 'ARMATURE':
                self.target_avatar = obj
                break

        # Set target avatar action to match source action
        self.target_avatar.animation_data.action = self.source_action

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: blender --background --python importAnim.py -- <path_to_glb>")
        sys.exit(1)
    
    glb_filepath = sys.argv[sys.argv.index("--") + 1]
    importer = GLBImporter(glb_filepath)
    importer.import_glb()


# # Second example ussage:
# importer = GLBImporter()
# importer.find_action_body()
# importer.find_shape_key_animation()
# print(importer.action, importer.shape_key_action)
# print()
# transfer = AnimationTransfer(importer.action, importer.shape_key_action, bpy.data.collections["mainAvatar"])
# transfer.transfer_bone_animation()