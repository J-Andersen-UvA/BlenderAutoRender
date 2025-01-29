import bpy
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)  # Add current directory

import renderCameras as rc
import importAnim as ia

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

# Load the .glb file, load all relevant animations, and transfer them to the target avatar. Then remove the imported collection
print("Importing the following .glb file:", glb_file)
importer = ia.GLBImporter(glb_file)
importer.find_action_body()
importer.find_shape_key_animation()
print("Imported the following animations:", importer.action, importer.shape_key_action)
transfer = ia.AnimationTransfer(importer.action, importer.shape_key_action, bpy.data.collections["mainAvatar"])
print("Transferring animations...")
transfer.transfer_bone_animation()
transfer.transfer_shape_key_animation()
importer.remove_collection_and_contents()

# Optional: Render the scene
render = 'True'
if '--render' in argv:
    render = argv[argv.index('--render') + 1]

if render == 'True':
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

    if '--render_samples' in argv:
        samples = int(argv[argv.index('--render_samples') + 1])
        camera_renderer.set_render_samples(samples)

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
