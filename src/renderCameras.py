import bpy
import os
from datetime import datetime
import argparse
import sys

class CamerasRenderer:
    def __init__(self, output_dir, render_engine="CYCLES"):
        """
        Initialize the CamerasRenderer with an output directory and render engine.

        :param output_dir: Path to the directory where rendered frames will be saved.
        :param render_engine: Render engine to use ("CYCLES" or "BLENDER_EEVEE").
        """
        self.base_output_dir = output_dir
        self.scene = bpy.context.scene
        self.set_render_engine(render_engine)
        self.output_dir = self.create_incremental_output_dir()

    def set_render_engine(self, render_engine):
        """
        Set the render engine for the scene.

        :param render_engine: Render engine to use ("CYCLES" or "BLENDER_EEVEE").
        """
        if render_engine.upper() not in ["CYCLES", "BLENDER_EEVEE"]:
            raise ValueError("Invalid render engine. Choose 'CYCLES' or 'BLENDER_EEVEE'.")
        self.scene.render.engine = render_engine.upper()

    def create_incremental_output_dir(self):
        """
        Create an incremental output directory to avoid overwriting previous renders.

        :return: Path to the created incremental output directory.
        """
        date_folder = datetime.now().strftime("%d_%m_%Y")
        base_path = os.path.join(self.base_output_dir, date_folder)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # Find the next incremental folder
        i = 1
        while True:
            incremental_path = os.path.join(base_path, str(i))
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
