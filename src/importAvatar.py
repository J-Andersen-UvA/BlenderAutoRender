import bpy
import sys

def import_glb(filepath):
    bpy.ops.import_scene.gltf(filepath=filepath)

if __name__ == "__main__":
    # Get the command line arguments
    argv = sys.argv

    # Blender's own arguments end with '--', so we need to find it
    if '--' not in argv:
        print("Error: No command line arguments found")
        sys.exit(1)

    # All arguments after '--' are user-defined
    argv = argv[argv.index('--') + 1:]

    if len(argv) < 1:
        print("Error: No GLB file path provided")
        sys.exit(1)

    glb_filepath = argv[0]

    # Import the GLB file
    import_glb(glb_filepath)