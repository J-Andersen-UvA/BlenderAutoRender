import bpy
import os
from datetime import datetime
import argparse
import sys

class CamerasRenderer:
    def __init__(self, output_dir, render_engine="CYCLES", output_format="PNG", compute_device_type='OPTIX', incr_folder_prefix=""):
        """
        Initialize the CamerasRenderer with an output directory and render engine.

        :param output_dir: Path to the directory where rendered frames will be saved.
        :param render_engine: Render engine to use ("CYCLES" or "BLENDER_EEVEE").
        """
        self.base_output_dir = output_dir
        self.scene = bpy.context.scene
        self.compute_device_type = compute_device_type
        self.set_render_engine(render_engine)
        self.output_dir = self.__create_incremental_output_dir(incr_folder_prefix)
        self.set_output_format(output_format)

    def set_output_format(self, output_format):
        """
        Set the output format for rendering.

        :param output_format: Output format to use (e.g., "PNG", "JPEG", "FFMPEG", etc.).
        """
        self.scene.render.image_settings.file_format = output_format

    def set_render_engine(self, render_engine):
        """
        Set the render engine for the scene.

        :param render_engine: Render engine to use ("CYCLES" or "BLENDER_EEVEE").
        """
        if render_engine.upper() not in ["CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"]:
            raise ValueError("Invalid render engine. Choose 'CYCLES' or 'BLENDER_EEVEE' or 'BLENDER_WORKBENCH'.")
        self.scene.render.engine = render_engine.upper()

        if render_engine.upper() == "CYCLES":
            self.__enable_gpu_rendering()

    def __enable_gpu_rendering(self):
        # Check if CUDA, OptiX, or HIP is available
        prefs = bpy.context.preferences.addons['cycles'].preferences
        devices = prefs.devices

        # Enable GPU compute
        if self.compute_device_type not in ['CUDA', 'OPTIX', 'HIP']:
            print("Invalid compute device type. Choose 'CUDA', 'OPTIX', or 'HIP'.\nFalling back to 'OPTIX'.")
            prefs.compute_device_type = 'OPTIX'
        else:
            prefs.compute_device_type = self.compute_device_type

        bpy.context.scene.cycles.device = 'GPU'

        # Activate all GPU devices
        for device in devices:
            device.use = True

    def set_resolution(self, width, height):
        """
        Set the resolution for rendering.

        :param width: Width of the rendered frames.
        :param height: Height of the rendered frames.
        """
        self.scene.render.resolution_x = width
        self.scene.render.resolution_y = height

    def set_render_samples(self, samples):
        """
        Set the number of samples for rendering.

        :param samples: Number of samples to use for rendering.
        """
        if samples < 128:
            print("Warning: Low sample count may result in noisy renders.")

        if self.scene.render.engine != 'CYCLES':
            print("Warning: Sample count is only relevant for Cycles render engine. Ignoring request...")
            return

        self.scene.cycles.samples = samples

    def __create_incremental_output_dir(self, incr_folder_prefix=""):
        """
        Create an incremental output directory to avoid overwriting previous renders.

        :return: Path to the created incremental output directory.
        """
        date_folder = datetime.now().strftime("%d_%m_%Y")
        base_path = os.path.join(self.base_output_dir, date_folder)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # Find the next incremental folder
        path = os.path.join(base_path, incr_folder_prefix)
        i = 1
        while True:
            incr_str = f"render_{i}"
            incremental_path = os.path.join(path, incr_str)
            if not os.path.exists(incremental_path):
                os.makedirs(incremental_path)
                return incremental_path
            i += 1

    def set_frame_range(self, start_frame, end_frame):
        """
        Set the frame range for rendering.

        :param start_frame: The first frame to render.
        :param end_frame: The last frame to render.
        """
        self.scene.frame_start = start_frame
        self.scene.frame_end = end_frame

    def render_camera(self, camera):
        """
        Render animation frames for a given camera.

        :param camera: Camera object to render from.
        """
        camera_output_path = os.path.join(self.output_dir, camera.name)
        if not os.path.exists(camera_output_path):
            os.makedirs(camera_output_path)
        self.scene.render.filepath = os.path.join(camera_output_path, "frame_")
        bpy.ops.render.render(animation=True)

    def render_all_cameras(self):
        """
        Render all cameras in the 'Cameras' collection.
        """
        cameras_collection = bpy.data.collections.get("Cameras")
        if not cameras_collection:
            print("No 'Cameras' collection found")
            return

        for obj in cameras_collection.objects:
            if obj.type == 'CAMERA':
                self.render_camera(obj)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render animations from all cameras in the 'Cameras' collection.")
    parser.add_argument("output_dir", type=str, help="Directory where rendered frames will be saved.")
    parser.add_argument("--render_engine", type=str, default="CYCLES", choices=["CYCLES", "BLENDER_EEVEE"],
                        help="Render engine to use (default: CYCLES).")
    parser.add_argument("--start_frame", type=int, default=bpy.context.scene.frame_start,
                        help="Start frame for rendering (default: scene's start frame).")
    parser.add_argument("--end_frame", type=int, default=bpy.context.scene.frame_end,
                        help="End frame for rendering (default: scene's end frame).")

    # Adjust argument parsing to handle Blender's "--" separator
    if "--" in sys.argv:
        args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    else:
        args = parser.parse_args()

    renderer = CamerasRenderer(args.output_dir, args.render_engine)
    renderer.set_frame_range(args.start_frame, args.end_frame)
    renderer.render_all_cameras()
