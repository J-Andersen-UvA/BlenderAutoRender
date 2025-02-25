import bpy

# For a given mesh, this script will find the material node with a label (default: viconColor)
# Then the color will be altered based on a provided hexadecimal string
def set_color_mesh_mat(mesh, color, label='viconColor'):
    # Convert hex color to RGB
    color = color.lstrip('#')
    rgb = tuple(int(color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    if mesh is not None:
        for mat in mesh.data.materials:
            if mat is not None and mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.label == label:
                        node.inputs['Base Color'].default_value = (*rgb, 1.0)
                        break
