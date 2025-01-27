import bpy
import sys
import os

# Parse arguments passed after '--'
argv = sys.argv[sys.argv.index("--") + 1:]  # Get arguments after '--'

# Required arguments
glb_file = argv[0]  # Path to the .glb file
output_folder = argv[1]  # Path to the output folder

# Optional arguments
background_path = None
timestretch = None

if '--background_path' in argv:
    background_path = argv[argv.index('--background_path') + 1]

if '--timestretch' in argv:
    target_fps = int(argv[argv.index('--timestretch') + 1])
    old_fps = int(argv[argv.index('--timestretch') + 2])
    timestretch = (target_fps, old_fps)

# Load the .glb file
bpy.ops.import_scene.gltf(filepath=glb_file)

# Optional: Replace the background
if background_path:
    # Prepare arguments for the script
    sys.argv = [__file__, "--", background_path]
    # Run the background script
    bpy.ops.script.python_file_run(filepath=os.path.join(os.path.dirname(__file__), "replaceBackground.py"))

# Optional: Apply time-stretching
if timestretch:
    target_fps, old_fps = timestretch
    # Prepare arguments for the script
    sys.argv = [__file__, "--", str(target_fps), str(old_fps)]
    # Run the time-stretching script
    bpy.ops.script.python_file_run(filepath=os.path.join(os.path.dirname(__file__), "timeStretch.py"))

# # Example: Render the scene
# output_file = os.path.join(output_folder, os.path.basename(glb_file).replace('.glb', '.png'))
# bpy.context.scene.render.filepath = output_file
# bpy.ops.render.render(write_still=True)

# # Save the .blend file (optional, for debugging or later use)
# blend_output_file = os.path.join(output_folder, os.path.basename(glb_file).replace('.glb', '.blend'))
# bpy.ops.wm.save_as_mainfile(filepath=blend_output_file)

# # Quit Blender
# bpy.ops.wm.quit_blender()
