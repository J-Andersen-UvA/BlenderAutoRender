import bpy
import sys

def replace_background(glb_path):
    # Find the "Background" collection
    background_collection = bpy.data.collections.get("Background")
    
    if background_collection is None:
        print("Background collection not found.")
        return
    
    # Remove all objects in the "Background" collection
    for obj in background_collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    # Import the GLB file
    bpy.ops.import_scene.gltf(filepath=glb_path)
    
    # Move imported objects to the "Background" collection
    imported_objects = [obj for obj in bpy.context.selected_objects]
    for obj in imported_objects:
        background_collection.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:]

    if len(argv) < 1 or len(argv) > 1:
        print("Usage: replaceBackground.py <path_to_glb>")
    else:
        glb_path = sys.argv[0]
        replace_background(glb_path)
