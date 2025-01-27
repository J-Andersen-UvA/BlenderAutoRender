import bpy
import os
import sys

def render_camera(camera, output_dir):
    scene = bpy.context.scene
    scene.camera = camera
    output_path = os.path.join(output_dir, camera.name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    scene.render.filepath = os.path.join(output_path, "frame_")
    bpy.ops.render.render(animation=True)

def main(output_dir):
    cameras_collection = bpy.data.collections.get("Cameras")
    if not cameras_collection:
        print("No 'Cameras' collection found")
        return

    for obj in cameras_collection.objects:
        if obj.type == 'CAMERA':
            render_camera(obj, output_dir)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: renderCameras.py <output_dir>")
    else:
        output_dir = sys.argv[2]
        main(output_dir)
