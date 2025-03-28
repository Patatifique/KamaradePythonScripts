import maya.cmds as cmds

# Written by Hubert Chauvaux, 26/11/2024

def transfer_uvs_from_group():
    
    """
    Transfers UVs from objects of selected source group to objects with same names from all other selected groups
    """
    
    # Get selected groups
    selection = cmds.ls(selection=True, type='transform')
    
    if len(selection) < 2:
        cmds.warning("Please select at least two groups: one source group followed by one or more target groups.")
        return
    
    # The first selected group is the source group
    source_group = selection[0]
    # The rest are target groups
    target_groups = selection[1:]
    
    # Get objects under the source group
    source_objects = cmds.listRelatives(source_group, children=True, type='transform', fullPath=True) or []
    
    if not source_objects:
        cmds.warning(f"No objects found in the source group: {source_group}.")
        return
    
    # Create a mapping of base names to full paths for the source objects
    source_mapping = {obj.split('|')[-1]: obj for obj in source_objects}
    
    # Iterate over each target group
    for target_group in target_groups:
        # Get objects under the target group
        target_objects = cmds.listRelatives(target_group, children=True, type='transform', fullPath=True) or []
        
        if not target_objects:
            cmds.warning(f"No objects found in the target group: {target_group}. Skipping.")
            continue
        
        # Match and transfer UVs
        for target_object in target_objects:
            target_name = target_object.split('|')[-1]
            
            # Check if there's a matching source object
            if target_name in source_mapping:
                source_object = source_mapping[target_name]
                try:
                    cmds.transferAttributes(source_object, target_object,
                                            transferUVs=2,  # Transfer UVs only
                                            transferColors=0,
                                            sampleSpace=4,  # World space
                                            sourceUvSet="map1",
                                            targetUvSet="map1",
                                            searchMethod=3,  # Closest to point
                                            flipUVs=False)
                    print(f"Transferred UVs from {source_object} to {target_object}.")
                except Exception as e:
                    cmds.warning(f"Failed to transfer UVs from {source_object} to {target_object}: {e}")
            else:
                print(f"No matching source object for {target_object}. Skipping.")
    
    cmds.inViewMessage(statusMessage="UV transfer completed!", fade=True)

def transfer_uvs_from_selection():
    """
    Simple Transfer Uvs from maya, but works for transfering to multiple objects at once
    """
    
    
    # Get the selected objects
    selection = cmds.ls(selection=True, type='transform')
    
    if len(selection) < 2:
        cmds.warning("Please select at least two objects: one source object followed by one or more target objects.")
        return
    
    # The first selected object is the source
    source_object = selection[0]
    # The rest are target objects
    target_objects = selection[1:]
    
    # Transfer UVs from source to each target
    for target_object in target_objects:
        try:
            cmds.transferAttributes(source_object, target_object,
                                    transferUVs=2,  # Transfer UVs only
                                    transferColors=0,
                                    sampleSpace=4,  # World space
                                    sourceUvSet="map1",
                                    targetUvSet="map1",
                                    searchMethod=3,  # Closest to point
                                    flipUVs=False)
            print(f"Transferred UVs from {source_object} to {target_object}.")
        except Exception as e:
            cmds.warning(f"Failed to transfer UVs from {source_object} to {target_object}: {e}")
    
    cmds.inViewMessage(statusMessage="UV transfer completed!", fade=True)

def layout_objects_in_udims():
    
    """
    Automatically layouts UVS from different objects to different UDIMs
    """
    
    # Get the selected objects
    selection = cmds.ls(selection=True, type='transform')
    
    if not selection:
        cmds.warning("Please select at least one object.")
        return
    
    # Start UDIM tile index (1001 corresponds to the first UDIM)
    base_udim = 1001
    
    # Process each object
    for i, obj in enumerate(selection):
        # Calculate the tile position (u, v) based on UDIM
        udim = base_udim + i
        u = ((udim - 1001) % 10)  # Horizontal position in the grid
        v = ((udim - 1001) // 10)  # Vertical position in the grid
        
        try:
            # Move the object's UVs to the calculated UDIM
            cmds.polyEditUV(obj + ".map[*]", uValue=u, vValue=v)
            print(f"Moved {obj} to UDIM {udim} (u={u}, v={v}).")
        except Exception as e:
            cmds.warning(f"Failed to move UVs for {obj}: {e}")
    
    cmds.inViewMessage(statusMessage="UV layout completed!", fade=True)



# Plugin Entry Point
def initializePlugin(plugin):
    cmds.inViewMessage(statusMessage="Custom UV Tools Plugin Loaded", fade=True)

def uninitializePlugin(plugin):
    cmds.inViewMessage(statusMessage="Custom UV Tools Plugin Unloaded", fade=True)
