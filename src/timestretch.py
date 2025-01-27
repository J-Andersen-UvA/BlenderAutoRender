import bpy
import sys

def set_framerate(target_fps, old_fps):
    # Set the new frame rate
    bpy.context.scene.render.fps = target_fps
    
    # Calculate the time stretching values
    bpy.context.scene.render.frame_map_old = old_fps
    bpy.context.scene.render.frame_map_new = target_fps

if __name__ == "__main__":
    # Parse arguments passed after '--'
    argv = sys.argv[sys.argv.index("--") + 1:]

    if len(argv) < 1 or len(argv) > 2:
        print("Usage: blender --python timestretch.py -- <target_fps> <old_fps>")
    else:
        target_fps = int(argv[0])
        old_fps = int(argv[1])
        
        set_framerate(target_fps, old_fps)
        print(f"Framerate changed to {target_fps} and time stretching values updated.")
