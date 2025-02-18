import bpy
import os
import sys
plugin_directory = os.path.dirname(__file__)
src_directory = os.path.join(plugin_directory, "src")
sys.path.append(src_directory)
sys.path.append(r"C:\Users\VICON\Desktop\Code\BlenderAutoRender\BlenderAutoRender\src")
import importAnim
# from src import importAnim

bl_info = {
    "name": "GLB Importer and Animator",
    "blender": (3, 0, 0),
    "category": "Import-Export",
    "author": "Jari Andersen",
    "version": (1, 1),
    "description": "A tool to import GLB files and transfer animations to target avatars",
    "location": "View3D > Sidebar > GLB Importer",
    "warning": "",
    "support": "COMMUNITY",
}

# File Browser Operator
class IMPORT_OT_GLBBrowser(bpy.types.Operator):
    bl_idname = "import.glb_browser"
    bl_label = "Import GLB"
    bl_description = "Opens file browser to import a GLB file"
    bl_options = {'REGISTER', 'UNDO'}

    # Fix Pylance warning
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    __annotations__['filepath'] = bpy.props.StringProperty(subtype="FILE_PATH")  # Explicit property definition

    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}
        
        if not self.filepath.lower().endswith(".glb") and not self.filepath.lower().endswith(".fbx"):
            self.report({'ERROR'}, "Please select a .glb or .fbx file")
            return {'CANCELLED'}

        # Import the GLB
        importer = importAnim.AnimImporter(filepath=self.filepath)
        self.report({'INFO'}, "GLB Imported Successfully!")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Additional Functionality Operator
class RETARGET_FUNCS(bpy.types.Operator):
    bl_idname = "retarget.retarget_and_remove"
    bl_label = "Retarget and Remove"
    bl_description = "Runs retarget/remap functionalities on the imported GLB, skeletons need to be the same, shape keys need to be the same"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        importer = importAnim.AnimImporter(filepath="")
        importer.find_action_body()
        importer.find_shape_key_animation()
        print(importer.action, importer.shape_key_action)
        print()
        transfer = importAnim.AnimationTransfer(importer.action, importer.shape_key_action, bpy.data.collections["mainAvatar"])
        transfer.transfer_bone_animation()
        transfer.transfer_shape_key_animation()
        importer.remove_collection_and_contents()
        self.report({'INFO'}, "Retarget done!")
        return {'FINISHED'}

class RETARGET_NODE_ANIM(bpy.types.Operator):
    bl_idname = "retarget.node_anim"
    bl_label = "Node Anim"
    bl_description = "Retarget node animations to armature"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        transfer = importAnim.AnimationTransfer(None, None, bpy.data.collections["mainAvatar"])
        transfer.link_animation_nodes_to_armature(collection_name="importedAnimation")
        self.report({'INFO'}, "Node animations retargeted!")
        return {'FINISHED'}

# UI Panel
class VIEW3D_PT_GLBImporterPanel(bpy.types.Panel):
    bl_label = "GLB Importer"
    bl_idname = "VIEW3D_PT_glb_importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GLB Importer"

    def draw(self, context):
        layout = self.layout
        layout.operator("import.glb_browser", text="Import GLB")
        layout.operator("retarget.retarget_and_remove", text="Run retarget/remap")
        layout.operator("retarget.node_anim", text="Retarget node anims to armature")

# Register & Unregister
def register():
    bpy.utils.register_class(IMPORT_OT_GLBBrowser)
    bpy.utils.register_class(RETARGET_FUNCS)
    bpy.utils.register_class(VIEW3D_PT_GLBImporterPanel)
    bpy.utils.register_class(RETARGET_NODE_ANIM)

def unregister():
    bpy.utils.unregister_class(IMPORT_OT_GLBBrowser)
    bpy.utils.unregister_class(RETARGET_FUNCS)
    bpy.utils.unregister_class(VIEW3D_PT_GLBImporterPanel)
    bpy.utils.unregister_class(RETARGET_NODE_ANIM)

if __name__ == "__main__":
    register()
