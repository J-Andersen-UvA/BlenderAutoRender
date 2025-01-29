import os
import sys
import subprocess
import argparse

def launch_blender(blender_path, scene_path, input_folder, output_folder, deheaded=True, render_engine="CYCLES", background=None, timestretch=None, frame_range=None, output_format='PNG', render_resolution=[1920, 1080], render_samples=128, render=True, cameras_apply_modifiers='True', compute_device='OPTIX'):
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
                output_folder,  # Output folder for saving results
                render_engine,  # Render engine to use
            ])
            
            # Add optional background replacement
            if background:
                command.extend(['--background_path', background])
            
            # Add optional time-stretching parameters
            if timestretch:
                target_fps, old_fps = timestretch
                command.extend(['--timestretch', str(target_fps), str(old_fps)])
            
            # Add optional frame range
            if frame_range:
                start_frame, end_frame = frame_range
                command.extend(['--frame_range', str(start_frame), str(end_frame)])

            # Add optional output format
            command.extend(['--output_format', output_format])

            # Add optional render resolution
            command.extend(['--render_resolution', str(render_resolution[0]), str(render_resolution[1])])

            # Add optional render samples
            command.extend(['--render_samples', str(render_samples)])

            # Add optional render
            command.extend(['--render', str(render)])

            # Add optional cameras apply modifiers
            command.extend(['--cameras_apply_modifiers', str(cameras_apply_modifiers)])

            # Add optional compute device
            command.extend(['--compute_device', str(compute_device)])

            print(f"Running Blender command:\n{command}\n")
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
    parser.add_argument("--render_engine", type=str, default="CYCLES", choices=["CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH", "EEVEE", "BLENDER_EEVEE"],
                        help="Render engine to use (default: CYCLES).")

    # Optional arguments
    parser.add_argument('--background', type=str, help='Path to background .glb file to replace the scene background')
    parser.add_argument('--timestretch', nargs=2, metavar=('TARGET_FPS', 'OLD_FPS'), type=int, help='Apply time stretching with target and old FPS values')
    parser.add_argument('--frame_range', nargs=2, metavar=('START_FRAME', 'END_FRAME'), type=int, help='Set the frame range for rendering')
    parser.add_argument('--output_format', type=str, default='PNG', help='Output file format for rendered images', choices=['PNG', 'JPEG', 'WebP', 'OPEN_EXR', 'FFMPEG'])
    parser.add_argument('--render_resolution', type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'), help='Set the render resolution', default=[1920, 1080])
    parser.add_argument('--render_samples', type=int, help='Set the render samples for Cycles rendering', default=128)
    parser.add_argument('--render', type=str, help='debug value to set if no render is prefered', default='True')
    parser.add_argument('--cameras_apply_modifiers', type=str, help='Apply modifiers and constraints to cameras', default='True')
    parser.add_argument('--compute_device', type=str, help='Set the compute device for rendering', default='OPTIX', choices=['CUDA', 'OPTIX', 'OPENCL', 'NONE'])

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

    # Validate optional arguments
    if args.deheaded.lower() not in ['true', 'false']:
        print("Error: 'deheaded' argument must be 'true' or 'false'")
        sys.exit(1)
    else:
        args.deheaded = args.deheaded.lower() == 'true'
    
    if args.render_engine not in ['CYCLES', 'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'BLENDER_WORKBENCH', 'EEVEE']:
        print("Error: 'render_engine' argument must be 'CYCLES' or 'BLENDER_EEVEE' or 'BLENDER_EEVEE_NEXT' or 'BLENDER_WORKBENCH' or 'EEVEE'")
        sys.exit(1)
    if args.render_engine in ['BLENDER_EEVEE', 'EEVEE']:
        args.render_engine = 'BLENDER_EEVEE_NEXT'
    
    if args.background and not os.path.isfile(args.background):
        print(f"Background file not found: {args.background}")
        sys.exit(1)
    
    if args.timestretch:
        target_fps, old_fps = args.timestretch
        if target_fps <= 0 or old_fps <= 0:
            print("Error: FPS values must be positive integers")
            sys.exit(1)

    if args.frame_range:
        start_frame, end_frame = args.frame_range
        if start_frame < 0 or end_frame < 0:
            print("Error: Frame range values must be non-negative integers")
            sys.exit(1)
        elif end_frame < start_frame:
            print("Error: End frame must be greater than or equal to start frame")
            sys.exit(1)
    
    if args.output_format not in ['PNG', 'JPEG', 'WebP', 'OPEN_EXR', 'FFMPEG']:
        print("Error: 'output_format' argument must be 'PNG', 'JPEG', 'WebP', 'OPEN_EXR', or 'FFMPEG'")
        sys.exit(1)
    
    if args.render_resolution:
        width, height = args.render_resolution
        if width <= 0 or height <= 0:
            print("Error: Resolution values must be positive integers")
            sys.exit(1)

        # also print warning for weird resolutions
        if width % 2 != 0 or height % 2 != 0:
            print("Warning: Resolution values should be even numbers for better compatibility")

    if args.render_samples <= 0:
        print("Error: Render samples must be a positive integer")
        sys.exit(1)

    if args.render == 'False' or args.render == 'false':
        args.render = 'False'
        print("Rendering is set to FALSE, no render will be done")
    
    if args.cameras_apply_modifiers.lower() not in ['False', 'false']:
        args.cameras_apply_modifiers = 'True'

    if args.compute_device not in ['CUDA', 'OPTIX', 'OPENCL', 'NONE']:
        print("Error: 'compute_device' argument must be 'CUDA', 'OPTIX', 'OPENCL', or 'NONE'")
        sys.exit(1)
    
    # Launch Blender for each .glb file
    launch_blender(
        blender_path=blender_path,
        scene_path=scene_path,
        input_folder=input_folder,
        output_folder=output_folder,
        deheaded=args.deheaded,
        render_engine=args.render_engine,
        background=args.background,
        timestretch=args.timestretch,
        frame_range=args.frame_range,
        output_format=args.output_format,
        render_resolution=args.render_resolution,
        render_samples=args.render_samples,
        render=args.render,
        cameras_apply_modifiers=args.cameras_apply_modifiers,
        compute_device=args.compute_device
    )

if __name__ == "__main__":
    main()
