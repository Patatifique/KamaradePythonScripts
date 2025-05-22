# Kamarade Python Scripts

This is a series of scripts for my 5th year movie, **Kamarade**'s pipeline.  
It's not meant to be used outside of this specific use case, but feel free to take snippets from it to include in your own code!

Most of these scripts are for **Maya 2025**, but `KamaradeUpdater` is a standalone Python application for managing Windows files.

---

## Maya Script List

### `KamaradeExporter.py`

**Description**:  
Exports Alembic files for the objects  **Iouri**, **Kat**, **Props**, and **Cameras** based on the contents of the Maya scene.  
It provides a popup UI to let users select what they want to export and handles versioning automatically.

**Features**:
- UI popup to toggle export options (Iouri, Kat, Props, Cameras)
- Validates scene naming (`*_Anim.ma` or `*_Anim.mb`)
- Automatically finds and exports specific rig parts
- Detects and exports objects from a set named `Ramses_Publish`
- Renames cameras before export
- Exports cameras as both `.abc` and `.mb` files
- Organizes exports into versioned folders under the `_published` directory


---


### `IouriBakerforFx.py`

**Description**:  
Automates the setup and baking of the Iouri character's animation in Maya for export to Marvelous Designer and Houdini. This script is specifically designed for the Kamarade pipeline and ensures that all relevant controllers, pose data, and animation are properly prepared and cleaned before export.

**Features**:
- Selects all Iouri controllers within the scene hierarchy

  
- Switches arm controls between FK and IK as needed
- Loads and applies a specific pose from a JSON file at a designated frame
- Bakes animation for selected objects, including keyframe management and cleanup
- Removes unnecessary animation layers and trims keyframes outside the playback range
- Restores correct parent and orientation spaces for arms, hands, and legs, facilitating future export to Houdini and Marvelous
- Sets all keyframes to linear interpolation for export compatibility


---


### `ULTIMATE_EXPORTER.py`

**Description**:  
A simple script that combines the functionality of both the baking (`IouriBakerforFx.py`) and exporting (`KamaradeExporter.py`) scripts. It automates the process of preparing (baking) the animation and then exporting the results, streamlining the workflow into a single step for the Kamarade pipeline.

---


### `lights_reflet_01.py`

**Description**:  
A simple Maya script that duplicates the light group named `LGT` to create a new group called `LGT_Reflet`, then removes any lights within the new group whose names contain "Rim" or "RIM". This is useful for quickly generating a reflection lighting setup without rim lights.


---


### `Mirror_Cam_V2.py`

**Description**:  
A Maya script for creating a mirrored version of a camera, useful for simulating reflections in scenes with reflective surfaces. The script first creates a controller (`Reflet_Ctrl`) to define the mirror plane. After positioning this controller, you select your camera and run the script again to generate a mirrored camera that matches the original's animation or static pose.

**Features**:
- Creates a rectangular controller to define the mirror surface
- Supports both static and animated cameras
- Duplicates and mirrors the selected camera's transform and keyframes relative to the controller
- Cleans up temporary objects after processing
- Outputs a new camera named `mirrored_<originalCamera>`

**Usage**:
1. Run the script once to create the `Reflet_Ctrl` controller.
2. Place `Reflet_Ctrl` flat against your reflective surface.
3. Select your camera and run the script again to create the mirrored camera.
4. The resulting mirrored camera needd to be flipped after rendering for correct orientation.


---


### `Sanity_Check_V02.py`

**Description**:  
A comprehensive Maya script that performs a series of automated checks to ensure your scene is ready for rendering according to the Kamarade pipeline standards. It validates render settings, color management, AOVs, Arnold imagers, render layers, texture color spaces, light setups, and more, providing clear feedback on any issues found.

**Features**:
- Checks render resolution and frame/animation file naming conventions
- Verifies color management and OCIO config path
- Ensures all required AOVs are present and correctly configured
- Validates Arnold imager settings and output suffixes
- Checks renderable cameras and Arnold render settings
- Validates render layer configurations and output settings
- Ensures texture nodes use the correct color spaces based on naming
- Checks light group visibility, HSV values, and aiAov attributes
- Detects meshes with display smooth mesh enabled (should be off)
- Summarizes all results, highlighting any failed checks with details


---


### `Shader_Assign_To_Abc.py`

**Description**:  
A Maya script that automates the assignment of shaders to Alembics avoiding the need for the currently buggy Alembic cache system in maya.

**Features**:
- Automatically finds the latest version of each shader by base name
- Assigns shaders to all relevant shapes and stand-ins in the current selection
- Handles multiple shader/shape groupings for complex assets
- Provides clear feedback for missing shaders, shading groups, or shapes


---


### `custom_UV_Tools`

**Description**:  
A set of custom Maya tools for streamlining UV transfer and layout workflows. This toolkit provides shelf buttons for quick access to batch UV transfer and automatic UDIM layout operations, making it easier to manage UVs across multiple objects and groups.

**Scripts**:

#### `UV_tools_setup.py`
- Adds custom buttons to the Maya UV Editing shelf for quick access to the UV tools.
- Each button runs a specific function from `custom_uv_tools.py`:

#### `scripts/custom_uv_tools.py`
- **transfer_uvs_from_selection**:  
  Transfers UVs from the first selected object to all other selected objects, supporting batch operations.
- **transfer_uvs_from_group**:  
  Transfers UVs from objects in a source group to objects with matching names in one or more target groups, automating group-based UV matching.
- **layout_objects_in_udims**:  
  Automatically arranges the UVs of selected objects into consecutive UDIM tiles, making multi-object texturing more efficient.
- Includes plugin entry/exit points for feedback when loaded or unloaded.
