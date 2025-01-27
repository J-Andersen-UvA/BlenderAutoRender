import os
import sys
import subprocess
import argparse

def launch_blender(blender_path, scene_path, input_folder, output_folder, deheaded=True, background=None, timestretch=None):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.glb'):
            file_path = os.path.join(input_folder, file_name)
            
            # Create the command to launch Blender
            command = [
                blender_path,
                scene_path,
            ]
            
            if deheaded:
                command.append('--background')
                
            command.extend([
                '--python', '/src/mainProcessing.py',  # The main script for handling all operations
                '--',  # Pass additional arguments after this
                file_path,  # Path to the .glb file
                output_folder  # Output folder for saving results
            ])
            
            # Add optional background replacement
            if background:
                command.extend(['--background_path', background])
            
            # Add optional time-stretching parameters
            if timestretch:
                target_fps, old_fps = timestretch
                command.extend(['--timestretch', str(target_fps), str(old_fps)])
            
            # Run the Blender command for this .glb file
            subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description="Blender Auto Render Script")

    # Required arguments
    parser.add_argument('--blender', type=str, default="C:/Program Files/Blender Foundation/Blender 4.3/blender.exe", help='Path to Blender executable')
    parser.add_argument('--scene', type=str, default='./renderScenes/Jake.blend', help='Path to default Blender scene')
    parser.add_argument('--input', type=str, default='./in', help='Input folder containing animation files')
    parser.add_argument('--output', type=str, default='./out', help='Output folder for rendered files')
    parser.add_argument('--deheaded', type=str, default='true', help='Run Blender in background mode')

    # Optional arguments
    parser.add_argument('--background', type=str, help='Path to background .glb file to replace the scene background')
    parser.add_argument('--timestretch', nargs=2, metavar=('TARGET_FPS', 'OLD_FPS'), type=int, help='Apply time stretching with target and old FPS values')

    args = parser.parse_args()

    blender_path = args.blender
    scene_path = os.path.abspath(args.scene)
    input_folder = os.path.abspath(args.input)
    output_folder = os.path.abspath(args.output)

    # Validate paths
    if not os.path.isfile(blender_path):
        print(f"Blender executable not found: {blender_path}")
        sys.exit(1)

    if not os.path.isfile(scene_path):
        print(f"Scene file not found: {scene_path}")
        sys.exit(1)

    if not os.path.isdir(input_folder):
        print(f"Input folder not found: {input_folder}")
        sys.exit(1)
    
    if not os.path.isdir(output_folder):
        print(f"Output folder not found: {output_folder}")
        sys.exit(1)

    if args.deheaded.lower() not in ['true', 'false']:
        print("Error: 'deheaded' argument must be 'true' or 'false'")
        sys.exit(1)
    else:
        args.deheaded = args.deheaded.lower() == 'true'

    # Launch Blender for each .glb file
    launch_blender(
        blender_path=blender_path,
        scene_path=scene_path,
        input_folder=input_folder,
        output_folder=output_folder,
        deheaded=args.deheaded,
        background=args.background,
        timestretch=args.timestretch
    )

if __name__ == "__main__":
    main()
