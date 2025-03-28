"""

Sanity Check Script for Maya 2025

=================================

This script performs a series of checks to ensure that a Maya scene meets specific requirements for rendering and animation.



Checks performed:

-----------------

1. Render Resolution: Verify if the resolution is set to 1920x804 (can be changed manually to what you want :)).

2. Frame/Animation ext: Ensure the file naming follows the 'name_#.ext' convention.

3. Color Management: Confirm that color management is enabled and the OCIO config path is correct.

4. AOVs: Check that all required AOVs are configured correctly.

5. Arnold Imagers: Verify the presence and settings of Arnold imagers.

6. Render Layers: Validate render layer settings, including renderable cameras and output configurations.

7. Texture Color Space: Ensure texture nodes use the appropriate color spaces based on naming conventions.

8. Lights: Confirm that light groups are visible, check HSV values of lights, and verify the `aiAov` attribute.



The script provides a summary of all checks, indicating which have passed and which have failed, with details for any issues.

"""

import maya.cmds as cmds

import mtoa.aovs as aovs

import colorsys


def check_render_resolution():
    """Check if the render resolution is set to 1920x804."""
    width = cmds.getAttr("defaultResolution.width")
    height = cmds.getAttr("defaultResolution.height")
    
    # Set This for a different resolution if needed     
    target_width = 1920
    target_height = 804

    if width == target_width and height == target_height:
        return True, None
    else:
        return False, f"Render resolution is incorrect! Current: {width}x{height}, Expected: {target_width}x{target_height}."
        
def check_frame_animation_ext():
    """Check if Frame/Animation ext is set to 'name_♯.ext'."""
    animation_enabled = cmds.getAttr("defaultRenderGlobals.animation")
    put_frame_before_ext = cmds.getAttr("defaultRenderGlobals.putFrameBeforeExt")
    period_in_ext = cmds.getAttr("defaultRenderGlobals.periodInExt")
    
    if animation_enabled and put_frame_before_ext == 1 and period_in_ext == 2:
        return True, None
    else:
        return False, (
            f"Frame/Animation ext is incorrect! Current settings: "
            f"animation={animation_enabled}, putFrameBeforeExt={put_frame_before_ext}, "
            f"periodInExt={period_in_ext}. Expected: 'name_#.ext'."
        )

def check_color_management_settings():
    """Check if color management is enabled and OCIO Config Path is set correctly."""
    
    # You can set your own path here if you want
    expected_path = "S:/SIC3D/SIC5/Projects/KAMARADE/aces_1.2/config.ocio"
    
    # Check if color management is enabled
    color_management_enabled = cmds.colorManagementPrefs(query=True, cmEnabled=True)
    
    if not color_management_enabled:
        return False, "Color Management is not enabled!"

    # Check the OCIO Config Path
    ocio_path = cmds.colorManagementPrefs(query=True, configFilePath=True)

    if ocio_path != expected_path:
        return False, (
            f"OCIO Config Path is incorrect! Current: '{ocio_path}', Expected: '{expected_path}'."
        )
    
    return True, None
        
        
def check_render_aovs():
    """Check if all required AOVs are correctly configured in the render settings."""
    required_aovs = [
        {"name": "ID", "data": "uint", "driver": "<exr>", "filter": "closest"},
        {"name": "N", "data": "vector", "driver": "<exr>", "filter": "closest"},
        {"name": "P", "data": "vector", "driver": "<exr>", "filter": "closest"},
        {"name": "RGBA", "data": "rgba", "driver": "<exr>", "filter": "gaussian"},
        {"name": "Z", "data": "float", "driver": "<exr>", "filter": "closest"},
        {"name": "albedo", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "crypto_asset", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "crypto_material", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "crypto_object", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "diffuse", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "emission", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "motionvector", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "specular_direct", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "specular_indirect", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
        {"name": "transmission", "data": "rgb", "driver": "<exr>", "filter": "gaussian"},
    ]

    # Get the list of existing AOVs
    aovs_list = aovs.AOVInterface().getAOVNodes(names=True)

    # Extract the AOV names from the list (the first element in the tuple)
    existing_aov_names = [aov[0] for aov in aovs_list]

    failed_aovs = []

    # Check if each required AOV is configured
    for aov in required_aovs:
        if aov["name"] not in existing_aov_names:
            failed_aovs.append(f"AOV '{aov['name']}' is missing!")
            
    # Check if RGBA AOV has the correct lightGroups attribute
    rgba_aov_node = f"aiAOV_{'RGBA'}"
    if cmds.objExists(rgba_aov_node):
        if cmds.attributeQuery("lightGroups", node=rgba_aov_node, exists=True):
            light_groups_value = cmds.getAttr(f"{rgba_aov_node}.lightGroups")
            if light_groups_value != 1:
                failed_aovs.append(f"RGBA AOV 'lightGroups' is incorrect! Found: {light_groups_value}, expected: True.")
        else:
            failed_aovs.append("RGBA AOV is missing the 'lightGroups' attribute!")
    else:
        failed_aovs.append("RGBA AOV node does not exist!")

    if failed_aovs:
        return False, "\n".join(failed_aovs)
    else:
        return True, None

def check_arnold_imagers():
    """Ensure the only imager is aiImagerDenoiserOidn1 with a valid layer selection and correct output suffix."""
    import maya.cmds as cmds

    expected_imager = "aiImagerDenoiserOidn1"
    required_suffix = "_denoise"

    # Get all imagers connected to the Arnold render options
    imagers = cmds.listConnections("defaultArnoldRenderOptions.imagers", source=True, destination=False) or []

    if not imagers:
        return False, "No imagers are connected to the Arnold render options!"

    if len(imagers) > 1:
        return False, f"Too many imagers connected! Found: {', '.join(imagers)}. Expected only: {expected_imager}."

    # Ensure the imager is the expected one
    if imagers[0] != expected_imager:
        return False, f"Incorrect imager connected! Found: {imagers[0]}. Expected: {expected_imager}."

    # Check that something is written in the layer selection
    layer_selection = cmds.getAttr(f"{expected_imager}.layerSelection").strip()
    if not layer_selection:
        return False, f"Layer selection is empty for {expected_imager}! It must contain some value."

    # Check that outputSuffix ends with the required suffix
    output_suffix = cmds.getAttr(f"{expected_imager}.outputSuffix").strip()
    if not output_suffix.endswith(required_suffix):
        return False, (
            f"Output suffix is incorrect for {expected_imager}! "
            f"Found: '{output_suffix}', expected to end with '{required_suffix}'."
        )

    return True, None


def check_render_settings():
    """Ensure that key render settings in Arnold are correctly configured."""
    settings = {
        "defaultArnoldRenderOptions.lowLightThreshold": 0.015,
    }

    # Check for renderable cameras
    renderable_cameras = [cam for cam in cmds.ls(type="camera") if cmds.getAttr(cam + ".renderable")]

    if not renderable_cameras:
        return False, "No renderable cameras found in the scene!"

    # Check the Arnold render settings
    for attr, expected_value in settings.items():
        if not cmds.objExists(attr):
            return False, f"Attribute {attr} does not exist!"

        current_value = cmds.getAttr(attr)

        # Round both values to 2 decimal places for a more forgiving check
        if round(current_value, 2) != round(expected_value, 2):
            return False, f"{attr} is incorrect! Found: {current_value}, expected: {expected_value}."

    return True, None

def check_render_layers():
    """Check for valid renderable cameras, render output settings, active layers, and master layer status per render layer."""
    layers = cmds.ls(type="renderLayer")

    if not layers:
        return False, "❌ No render layers found!"

    # Store the current render layer
    current_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)

    all_passed = True
    errors = []

    for layer in layers:
        try:
            cmds.editRenderLayerGlobals(currentRenderLayer=layer)
        except RuntimeError:
            errors.append(f"⚠️ Skipping layer '{layer}' because it cannot be activated.")
            continue

        # ✅ Skip the defaultRenderLayer from the general active layer check
        if layer != "defaultRenderLayer" and not cmds.getAttr(f"{layer}.renderable"):
            errors.append(f"Layer '{layer}' is not active.")
            all_passed = False

        # ✅ Check Renderable Cameras
        renderable_cameras = [cam for cam in cmds.ls(type="camera") if cmds.getAttr(cam + ".renderable")]

        if len(renderable_cameras) > 2:
            errors.append(f"More than 2 renderable cameras in layer '{layer}': {renderable_cameras}.")
            all_passed = False
        elif len(renderable_cameras) == 2 and not any(cam.startswith("mirrored_") for cam in renderable_cameras):
            errors.append(f"Two renderable cameras in layer '{layer}', but none start with 'mirrored_': {renderable_cameras}.")
            all_passed = False
            
            

        # ✅ Check Render Output Settings
        half_precision = cmds.getAttr("defaultArnoldDriver.halfPrecision")
        autocrop = cmds.getAttr("defaultArnoldDriver.autocrop")
        merge_aovs = cmds.getAttr("defaultArnoldDriver.mergeAOVs")
        tiled = cmds.getAttr("defaultArnoldDriver.tiled")

        if layer.startswith("rs_GLOBAL_"):
            # Special case: Layers starting with GLOBAL_ allow halfPrecision=False
            if autocrop and merge_aovs and not tiled:
                if not half_precision:
                    continue  # Global layer with valid settings
                else:
                    errors.append(
                        f"Render output settings incorrect in layer '{layer}'! "
                        f"halfPrecision={half_precision}, autocrop={autocrop}, "
                        f"mergeAOVs={merge_aovs}, tiled={tiled}. "
                        f"Expected for GLOBAL_: halfPrecision=False, autocrop=True, mergeAOVs=True, tiled=False."
                    )
                    all_passed = False
            else:
                errors.append(
                    f"Render output settings incorrect in layer '{layer}'! "
                    f"halfPrecision={half_precision}, autocrop={autocrop}, "
                    f"mergeAOVs={merge_aovs}, tiled={tiled}. "
                    f"Expected: autocrop=True, mergeAOVs=True, tiled=False."
                )
                all_passed = False
        else:
            # Standard settings for all other layers
            if not (half_precision and autocrop and merge_aovs and not tiled):
                errors.append(
                    f"Render output settings incorrect in layer '{layer}'! "
                    f"halfPrecision={half_precision}, autocrop={autocrop}, "
                    f"mergeAOVs={merge_aovs}, tiled={tiled}. "
                    f"Expected: halfPrecision=True, autocrop=True, mergeAOVs=True, tiled=False."
                )
                all_passed = False

        # ✅ Check if the master layer is deactivated (only for defaultRenderLayer)
        if layer == "defaultRenderLayer" and cmds.getAttr(f"{layer}.renderable"):
            errors.append(f"Master layer '{layer}' is still active. It should be deactivated.")
            all_passed = False

    # Restore the original render layer
    cmds.editRenderLayerGlobals(currentRenderLayer=current_layer)

    return all_passed, "\n".join(errors) if errors else None

    
def check_color_space_for_textures():
    """Check if textures are set to the correct color space based on texture names."""
    failed_checks = []

    # Get all file textures in the scene
    file_nodes = cmds.ls(type='file')

    if not file_nodes:
        return False, "No file textures found in the scene."

    for file_node in file_nodes:
        if cmds.objExists(file_node):  # Ensure the file node exists
            file_name = cmds.getAttr(file_node + ".fileTextureName")
            color_space = cmds.getAttr(file_node + ".colorSpace")

            # Check for textures with "ACES" in the name
            if "ACES" in file_name:
                if color_space != "ACES - ACEScg":
                    failed_checks.append(f"Texture '{file_node}' should be set to 'ACES - ACEScg'. Current: {color_space}.")

            # Check for textures with "Raw" in the name
            if "Raw" in file_name:
                if color_space != "Utility - Raw":
                    failed_checks.append(f"Texture '{file_node}' should be set to 'Utility - Raw'. Current: {color_space}.")

    # Return the results
    if failed_checks:
        return False, "\n".join(failed_checks)
    else:
        return True, None


def check_lights():
    """Check if each group starting with 'LGT' has visibility turned on, and check light shapes HSV values and aiAov attribute."""
    # List all objects in the scene
    all_objects = cmds.ls(dag=True, long=True)
    
    # Filter the objects to get only those starting with "|LGT" and have exactly one "|LGT" in their name, and have children
    light_groups = [
        obj for obj in all_objects
        if obj.startswith('|LGT') and obj.count('|LGT') == 1 and cmds.listRelatives(obj, children=True)
    ]
    
    # Check visibility for each light group
    failed_lights = []
    for light_group in light_groups:
        visibility = cmds.getAttr(f"{light_group}.visibility")
        if not visibility:
            failed_lights.append(f"Light group '{light_group}' has visibility turned off.")
    
    # Check light shapes HSV values and aiAov attribute
    failed_light_shapes = []
    all_transform_nodes = cmds.ls(type='transform', long=True)  # Use long names (full paths)
    
    for transform in all_transform_nodes:
        # Get the shape of the transform node
        shapes = cmds.listRelatives(transform, shapes=True, fullPath=True)
        
        if shapes:
            shape = shapes[0]
            shape_type = cmds.nodeType(shape)
            
            # Check if the shape is a light type (Arnold and standard lights)
            if shape_type in ['aiAreaLight', 'aiPointLight', 'aiSpotLight', 'directionalLight']:
                try:
                    # Get the color value (RGB) of the light shape
                    rgb_values = cmds.getAttr(shape + ".color")[0]  # RGB values as a tuple
                    
                    # Convert RGB to HSV
                    hsv_values = colorsys.rgb_to_hsv(rgb_values[0], rgb_values[1], rgb_values[2])
                    
                    # Check if the V value of HSV is above 1.0
                    if hsv_values[2] > 1.0:
                        failed_light_shapes.append(f"Light '{shape}' has HSV value 'V' above 1.0. V = {hsv_values[2]}")

                    # Check aiAov attribute for 'default' value
                    ai_aov = cmds.getAttr(f"{shape}.aiAov")
                    if ai_aov == "default":
                        failed_light_shapes.append(f"Light '{shape}' has aiAov set to 'default'.")

                except Exception as e:
                    failed_light_shapes.append(f"Error with light shape '{shape}': {e}")
    
    if failed_lights or failed_light_shapes:
        return False, "\n".join(failed_lights + failed_light_shapes)
    else:
        return True, None
        
def check_display_smooth_mesh():
    """Check if any mesh shape has 'displaySmoothMesh' enabled (should be off)."""
    meshes = cmds.ls(type="mesh", long=True)  # Get all mesh shapes (long names)

    if not meshes:
        return True, None

    smooth_mesh_enabled = []

    for mesh in meshes:
        if cmds.attributeQuery("displaySmoothMesh", node=mesh, exists=True):
            value = cmds.getAttr(f"{mesh}.displaySmoothMesh")
            if value != 0:
                smooth_mesh_enabled.append(f"{mesh} (displaySmoothMesh={value})")

    if smooth_mesh_enabled:
        return False, "The following mesh shapes have 'displaySmoothMesh' enabled:\n" + "\n".join(smooth_mesh_enabled)

    return True, None


def run_sanity_checks():
    """Run all sanity checks and summarize results."""
    checks = [
        check_render_resolution,
        check_frame_animation_ext,
        check_color_management_settings,
        check_render_settings,
        check_render_aovs,
        check_arnold_imagers,
        check_color_space_for_textures,
        check_lights,
        check_display_smooth_mesh,
        
        # PERFORMANCE HEAVY -- Turn off if you wanna check anything else than render layers
        check_render_layers,
        
    ]
    
    all_passed = True
    for check in checks:
        passed, error_message = check()
        if not passed:
            print(f"❌ {error_message}")
            all_passed = False

    if all_passed:
        print("\n🎉 All checks passed!")
    else:
        print("\n⚠️ Some checks failed. See messages above for details.")

# Run the sanity check script
if __name__ == "__main__":
    run_sanity_checks()

#########################################################################################################