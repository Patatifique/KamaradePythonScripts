import maya.cmds as cmds
import custom_uv_tools

# Written by Hubert Chauvaux, 26/11/2024

def add_buttons_to_uv_editing_shelf():
    # Name of the default UV Editing shelf
    shelf_name = "UVEditing"

    # Check if the UV Editing shelf exists
    if not cmds.shelfLayout(shelf_name, exists=True):
        cmds.warning(f"Shelf '{shelf_name}' does not exist. Please ensure the UV Editing shelf is loaded.")
        return

    # Add buttons for each tool
    cmds.shelfButton(
        command="import custom_uv_tools; custom_uv_tools.transfer_uvs_from_selection()",
        label="Transfer UVs",
        image="commandButton.png",  # Use a default for now but idk maybe i'll change it
        parent=shelf_name,
        annotation="Transfer UVs from one object to selected objects"
    )
    
    cmds.shelfButton(
        command="import custom_uv_tools; custom_uv_tools.transfer_uvs_from_group()",
        label="Transfer UVS from group selection",
        image="commandButton.png",  # Use a default for now but idk maybe i'll change it
        parent=shelf_name,
        annotation="Transfer UVs from objects of a group to objets from other selected groups"
    )
    
    cmds.shelfButton(
        command="import custom_uv_tools; custom_uv_tools.layout_objects_in_udims()",
        label="UDIM Layout",
        image="commandButton.png",  # Use a default for now but idk maybe i'll change it
        parent=shelf_name,
        annotation="Layout objects in UDIM tiles"
    )

    cmds.inViewMessage(statusMessage="Tools added to UV Editing shelf!", fade=True)

# Run the function to add buttons
add_buttons_to_uv_editing_shelf()
