# BlenderAutoRender
With the amount of animations we have gathered, it would be absolutely painful to render them all by hand. So lets automate this process :) 

## Command-Line Arguments
This section describes all the command-line arguments for the Blender Auto Render Script. Use these arguments to customize the rendering process.

### Required Arguments

| Argument  | Description                                                   | Default Value                                               |
|-----------|---------------------------------------------------------------|-------------------------------------------------------------|
| --blender | Path to the Blender executable.                               | C:/Program Files/Blender Foundation/Blender 4.3/blender.exe |
| --scene   | Path to the default Blender scene .blend file.                | ./renderScenes/Jake.blend                                   |
| --input   | Path to the input folder containing .glb files.               | ./in                                                        |
| --output  | Path to the output folder where rendered files will be saved. | ./out                                                       |

### Optional Arguments

|    Argument   |                                             Description                                            |            Example            |
|:-------------:|:--------------------------------------------------------------------------------------------------:|:-----------------------------:|
| --background  | Path to a .glb file to replace the background in the scene.                                        | --background ./background.glb |
| --timestretch | Apply time-stretching to animations. Provide the target FPS and the old FPS as two integer values. | --timestretch 60 30           |
