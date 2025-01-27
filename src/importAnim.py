import bpy
import sys

def import_glb(filepath):
    bpy.ops.import_scene.gltf(filepath=filepath, bone_dir='TEMPERANCE')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: blender --background --python importAnim.py -- <path_to_glb>")
        sys.exit(1)
    
    glb_filepath = sys.argv[sys.argv.index("--") + 1]
    import_glb(glb_filepath)
