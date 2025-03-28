# SCRIPT FOR MIRRORING A CAMERA IN MAYA 2025

# Running the script for the first time creates the controller.
# Place the controller flat against your reflective surface, select your camera and run the script again.
# The resulting mirrored camera needs to be flipped after rendering.

# Written by Hubert Chauvaux on 12/12/2024.




import maya.cmds as cmds

# CTRL creation logic
def create_rectangle_curve(length_x=1.0):
    """
    Creates a rectangle using curves in Maya.
    The Z-axis length will be half of the X-axis length.

    :param length_x: The length of the rectangle along the X-axis (default: 1.0).
    """
    # Calculate the Z-axis length as half of the X-axis length
    length_z = length_x / 2.0

    # Define the points for the rectangle
    points = [
        (-length_x / 2.0, 0, -length_z / 2.0),
        ( length_x / 2.0, 0, -length_z / 2.0),
        ( length_x / 2.0, 0,  length_z / 2.0),
        (-length_x / 2.0, 0,  length_z / 2.0),
        (-length_x / 2.0, 0, -length_z / 2.0)  # Close the rectangle
    ]

    # Create the curve
    curve = cmds.curve(p=points, d=1, name="rectangle_curve")

    # Rotate the curve by -90 degrees on the X-axis
    cmds.rotate(-90, 0, 0, curve, relative=True)

    # Freeze transformations
    cmds.makeIdentity(curve, apply=True, translate=True, rotate=True, scale=True, normal=False)

    # Output the curve name
    print(f"Created curve: {curve}")
    return curve


def mirror_camera_transform(camera_transform, reflet_ctrl):
    """
    Mirrors the position and rotation of a camera transform relative to the 'Reflet_Ctrl'.
    :param camera_transform: The camera transform to mirror.
    :param reflet_ctrl: The reference control object for mirroring.
    """
    # Create a locator to match the camera's position and rotation
    locator_transform = cmds.spaceLocator(name="transform_match_locator")[0]
    cmds.matchTransform(locator_transform, camera_transform)
    
    # Duplicate the Reflet_Ctrl and apply transformations
    reflet_temp_name = f"{camera_transform}_Reflet_Temp"
    reflet_temp = cmds.duplicate(reflet_ctrl, name=reflet_temp_name)[0]
    
    # Parent the locator to the reflected control
    cmds.parent(locator_transform, reflet_temp)
    
    # Scale Reflet Temp by -1 on the Z axis for mirroring
    cmds.setAttr(f"{reflet_temp}.scaleZ", -1)
    
    # Unparent the locator while preserving its transformation
    cmds.parent(locator_transform, world=True)    
    # Scale the locator by -1 on the X axis to complete the mirroring
    cmds.setAttr(f"{locator_transform}.scaleX", -1)
    
    return locator_transform, reflet_temp


import maya.cmds as cmds

# Updated create_mirrored_camera function to support animated cameras and cleanup locators
import maya.cmds as cmds

# Updated create_mirrored_camera function to support animated cameras and cleanup locators
def create_mirrored_camera():
    # Ensure a camera is selected
    selection = cmds.ls(selection=True, type="transform")
    if not selection or not cmds.listRelatives(selection[0], shapes=True, type="camera"):
        cmds.warning("Please select a camera transform.")
        return
    camera_transform = selection[0]

    # Check if the camera has keyframes
    keyframes = cmds.keyframe(camera_transform, query=True)
    if not keyframes:
        cmds.warning(f"Camera '{camera_transform}' has no keyframes. Creating a static mirrored camera.")
        # Handle static camera as before
        return create_mirrored_camera_static(camera_transform)

    # Define names for the new objects
    mirrored_camera_name = f"mirrored_{camera_transform}"

    # Delete the existing mirrored camera if it exists
    if cmds.objExists(mirrored_camera_name):
        cmds.delete(mirrored_camera_name)
        print(f"Deleted existing mirrored camera: {mirrored_camera_name}")

    # Duplicate the camera
    mirrored_camera = cmds.duplicate(camera_transform, name=mirrored_camera_name)[0]

    # Get the range of frames from the first to the last keyframe
    start_frame = min(keyframes)
    end_frame = max(keyframes)

    # Loop through each frame in the range (inclusive)
    for frame in range(int(start_frame), int(end_frame) + 1):
        cmds.currentTime(frame)

        # Create the mirrored locator and apply the mirror transformation
        locator_transform, reflet_temp = mirror_camera_transform(camera_transform, "Reflet_Ctrl")

        # Snap the mirrored camera to the locator for this frame
        cmds.matchTransform(mirrored_camera, locator_transform)

        # Set keyframe for the mirrored camera at the current frame
        cmds.setKeyframe(mirrored_camera)
        
        # Break the scale attribute connection for each axis
        for axis in ["X", "Y", "Z"]:
            scale_attr = f"{mirrored_camera}.scale{axis}"
            connections = cmds.listConnections(scale_attr, source=True, destination=False)
            if connections:
                for conn in connections:
                    cmds.disconnectAttr(f"{conn}.output", scale_attr)  # Disconnect the attribute
            
        # Freeze transformations on the mirrored camera
        cmds.makeIdentity(mirrored_camera, apply=True, scale=True)
        
        
        # Keyframe rotation again
        for attr in ["rotate"]:
            cmds.setKeyframe(f"{mirrored_camera}.{attr}")
        

        # Delete the locator and reflected control after use
        cmds.delete(locator_transform)
        cmds.delete(reflet_temp)

    print(f"Mirrored animated camera '{mirrored_camera}' created successfully.")

# Static mirrored camera function (for fallback)
def create_mirrored_camera_static(camera_transform):
    mirrored_camera_name = f"mirrored_{camera_transform}"

    # Delete the existing mirrored camera if it exists
    if cmds.objExists(mirrored_camera_name):
        cmds.delete(mirrored_camera_name)
        print(f"Deleted existing mirrored camera: {mirrored_camera_name}")

    # Call mirror logic and get the mirrored locator and reflected control
    locator_transform, reflet_temp = mirror_camera_transform(camera_transform, "Reflet_Ctrl")

    # Duplicate the camera
    mirrored_camera = cmds.duplicate(camera_transform, name=mirrored_camera_name)[0]

    # Snap the mirrored camera to the locator
    cmds.matchTransform(mirrored_camera, locator_transform)

    # Freeze transformations on the mirrored camera
    cmds.makeIdentity(mirrored_camera, apply=True, scale=True)

    # Clean up by deleting the temporary Reflet Temp object and the locator
    cmds.delete(reflet_temp)
    cmds.delete(locator_transform)

    print(f"Mirrored static camera '{mirrored_camera}' created successfully.")

# Check if Reflet_Ctrl exists, create it if it doesn't, run the script if it does
if not cmds.objExists("Reflet_Ctrl"):
    cmds.warning("'Reflet_Ctrl' does not exist. Creating it at world 0, please run the script again after placing it :).")
    reflet_ctrl = create_rectangle_curve(length_x=1.0)
    cmds.rename(reflet_ctrl, "Reflet_Ctrl")
    reflet_ctrl = "Reflet_Ctrl"
else:
    create_mirrored_camera()
