# BlenderAutoRender
With the amount of animations we have gathered, it would be absolutely painful to render them all by hand. So lets automate this process :) 

## Command-Line Arguments
This section describes all the command-line arguments for the Blender Auto Render Script. Use these arguments to customize the rendering process.

### Required Arguments

| Argument   | Description                                                   | Default Value                                               |
|------------|---------------------------------------------------------------|-------------------------------------------------------------|
| --blender  | Path to the Blender executable.                               | C:/Program Files/Blender Foundation/Blender 4.3/blender.exe |
| --scene    | Path to the default Blender scene .blend file.                | ./renderScenes/Jake.blend                                   |
| --input    | Path to the input folder containing .glb files.               | ./in                                                        |
| --output   | Path to the output folder where rendered files will be saved. | ./out                                                       |
| --deheaded | Run Blender in background mode. Set to 'true' or 'false'.     | true                                                        |

### Optional Arguments

|    Argument       | Description                                                                                     | Example                    |
|:-----------------:|:-----------------------------------------------------------------------------------------------:|:--------------------------:|
| --background      | Path to a .glb file to replace the background in the scene.                                     | --background ./background.glb |
| --timestretch     | Apply time-stretching to animations. Provide the target FPS and the old FPS as two integer values. | --timestretch 60 30        |
| --frame_range     | Set the frame range for rendering (start and end frames).                                        | --frame_range 1 250        |
| --output_format   | Output file format for rendered images (e.g., PNG, JPEG, WebP).                                  | --output_format FFMPEG     |
| --render_resolution | Set the render resolution (width and height).                                                 | --render_resolution 1920 1080 |
| --render_samples  | Set the number of render samples for Cycles rendering.                                           | --render_samples 128       |
| --render_engine   | Choose the render engine: CYCLES or BLENDER_EEVEE.                                               | --render_engine CYCLES     |