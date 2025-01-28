import bpy
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)  # Add current directory

import renderCameras as rc

# Parse arguments passed after '--'
argv = sys.argv[sys.argv.index("--") + 1:]  # Get arguments after '--'

# Required arguments
glb_file = argv[0]  # Path to the .glb file
output_folder = argv[1]  # Path to the output folder
render_engine = argv[2]  # Render engine to use ("CYCLES" or "BLENDER_EEVEE")

# Optional arguments
background_path = None
timestretch = None

# Optional: Replace the background
if '--background_path' in argv:
    background_path = argv[argv.index('--background_path') + 1]
    # Prepare arguments for the script
    sys.argv = [__file__, "--", background_path]
    # Run the background script
    bpy.ops.script.python_file_run(filepath=os.path.join(os.path.dirname(__file__), "optionalScripts/replaceBackground.py"))

# Optional: Apply time-stretching
if '--timestretch' in argv:
    target_fps = int(argv[argv.index('--timestretch') + 1])
    old_fps = int(argv[argv.index('--timestretch') + 2])
    timestretch = (target_fps, old_fps)
    target_fps, old_fps = timestretch
    # Prepare arguments for the script
    sys.argv = [__file__, "--", str(target_fps), str(old_fps)]
    # Run the time-stretching script
    bpy.ops.script.python_file_run(filepath=os.path.join(os.path.dirname(__file__), "optionalScripts/timeStretch.py"))

# Load the .glb file
bpy.ops.import_scene.gltf(filepath=glb_file)

# Render the scene
camera_renderer = rc.CamerasRenderer(output_folder, render_engine)
# Optional: Set the frame range
if '--frame_range' in argv:
    start_frame = int(argv[argv.index('--frame_range') + 1])
    end_frame = int(argv[argv.index('--frame_range') + 2])
    camera_renderer.set_frame_range(start_frame, end_frame)

if '--output_format' in argv:
    output_format = argv[argv.index('--output_format') + 1]
    camera_renderer.set_output_format(output_format)

if '--render_resolution' in argv:
    width = int(argv[argv.index('--render_resolution') + 1])
    height = int(argv[argv.index('--render_resolution') + 2])
    camera_renderer.set_resolution(width, height)

camera_renderer.render_all_cameras()

# Save the .blend file with the rendered results as a new file
# blend_output_file = os.path.join(output_folder, os.path.basename(glb_file).replace('.glb', '.blend'))
# # Check if file exists, if so, increment the name
# i = 1
# while os.path.exists(blend_output_file):
#     blend_output_file = blend_output_file.replace('.blend', f'_{i}.blend')
#     i += 1
# bpy.ops.wm.save_as_mainfile(filepath=blend_output_file)

# # Quit Blender
# bpy.ops.wm.quit_blender()
