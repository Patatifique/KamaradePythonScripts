import maya.cmds as cmds
import os

# Auto exports kat, iouri and props in the right place based on the name of file etc

# Global variables for export options
ExportIouri = True
ExportKat = True
ExportProps = True
ExportCameras = True
StartFrame = 901
export_done = False  # Flag to control execution


# POPUP DEF, It's also here that the other defs are called
def export_options_popup():
    global ExportIouri, ExportKat, ExportProps, ExportCameras, export_done

    def apply_settings(*args):
        """ Updates global variables and closes the UI. """
        global ExportIouri, ExportKat, ExportProps, ExportCameras, StartFrame, export_done
        ExportIouri = cmds.checkBox("cb_iouri", query=True, value=True)
        ExportKat = cmds.checkBox("cb_kat", query=True, value=True)
        ExportProps = cmds.checkBox("cb_props", query=True, value=True)
        ExportCameras = cmds.checkBox("cb_cameras", query=True, value=True)
        StartFrame = cmds.intField("start_frame", query=True, value=True)
        export_done = True  # Mark export as done
        cmds.deleteUI("export_options_win")
    
    # Delete existing UI if necessary
    if cmds.window("export_options_win", exists=True):
        cmds.deleteUI("export_options_win")

    # Create UI
    win = cmds.window("export_options_win", title="Export Options", widthHeight=(400, 250))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="Select export options:")
    cmds.checkBox("cb_iouri", label="Export Iouri", value=ExportIouri)
    cmds.checkBox("cb_kat", label="Export Kat", value=ExportKat)
    cmds.checkBox("cb_props", label="Export Props", value=ExportProps)
    cmds.checkBox("cb_cameras", label="Export Cameras", value=ExportCameras)
    cmds.text(label="Start Frame:")
    cmds.intField("start_frame", value=StartFrame)
    cmds.button(label="Apply", command=apply_settings)

    cmds.showWindow(win)

    # Wait until the user presses "Apply"
    def check_export_done():
        if export_done:
            # Continue with the rest of the script after Apply is pressed
            print(f"ExportIouri: {ExportIouri}, ExportKat: {ExportKat}, ExportProps: {ExportProps}, ExportCameras: {ExportCameras}, StartFrame: {StartFrame}")
            # Rename cameras if we export them
            if ExportCameras == True:
                rename_cameras()
            # Call the export function here
            export_alembic()
                
        else:
            cmds.scriptJob(runOnce=True, idleEvent=check_export_done)

    cmds.scriptJob(runOnce=True, idleEvent=check_export_done)

# Call the function to display the popup
export_options_popup()






# DEFS

def get_next_version_folder(base_path):
    """Finds the next available version folder inside the given base path."""
    version = 1
    while True:
        version_folder = os.path.join(base_path, f"V{version:02d}")
        if not os.path.exists(version_folder):
            os.makedirs(version_folder)
            return version_folder
        version += 1

def get_full_paths(objects):
    """Finds the full object paths in the scene matching the given list (ignoring namespaces)."""
    found_objects = []
    all_objects = cmds.ls(tr=True)  # Get all transform nodes
    for obj in objects:
        for full_obj in all_objects:
            if full_obj.endswith(obj):
                found_objects.append(full_obj)
    return found_objects
    
    
def rename_cameras():
    objects = cmds.ls("*_camera")  # Find all objects ending with '_camera'
    
    for obj in objects:
        new_name = "CAM_" + obj[:-7]  # Remove '_camera' and add 'CAM_'
        cmds.rename(obj, new_name)
        print(f"Renamed: {obj} -> {new_name}")


def export_abc(obj_list, export_name, version_folder, scene_name, start_frame, end_frame):
    """Exports selected objects to Alembic."""
    if not obj_list:
        cmds.warning(f"No objects found for {export_name} export!")
        return

    export_filename = "{}_{}.abc".format(scene_name.rsplit(".", 1)[0], export_name)
    full_export_path = os.path.join(version_folder, export_filename).replace("\\", "/")

    cmds.select(obj_list, replace=True)

    # Correctly format -root flags
    root_flags = " ".join(["-root " + obj for obj in obj_list])

    cmds.AbcExport(
        j=f"-frameRange {start_frame} {end_frame} -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa {root_flags} -file {full_export_path}"
    )

    print(f"Exported: {full_export_path}")

def select_cameras():
    """Selects cameras and mirrored objects."""
    # Get objects that start with "CAM" and "mirrored_"
    camera_objects = get_full_paths([obj for obj in cmds.ls(tr=True) if obj.startswith("CAM") or obj.endswith("_camera")])
    mirrored_objects = get_full_paths([obj for obj in cmds.ls(tr=True) if obj.startswith("mirrored_")])

    selected_cameras = camera_objects + mirrored_objects
    cmds.select(selected_cameras)

    return selected_cameras

def export_alembic():
    # Get the scene file name
    scene_name = cmds.file(q=True, sn=True, shn=True)
    
    if not scene_name or not (scene_name.endswith("_Anim.ma") or scene_name.endswith("_Anim.mb")):
        cmds.warning("Scene file must end with '_Anim.ma' or '_Anim.mb' to proceed!")
        return
    
    # Extract base name and remove file extension
    base_name = scene_name.rsplit("_Anim.", 1)[0]
    
    # Define export directory
    project_path = r"S:\SIC3D\SIC5\Projects\KAMARADE\05-SHOTS"
    shot_folder = os.path.join(project_path, base_name)
    anim_folder = os.path.join(shot_folder, scene_name.rsplit(".", 1)[0])
    publish_folder = os.path.join(anim_folder, "_published")

    # Get the next available version folder
    version_folder = get_next_version_folder(publish_folder)

    # Get the last frame of the current scene
    start_frame = StartFrame
    end_frame = int(cmds.playbackOptions(q=True, maxTime=True))

    # Get all objects in the scene with their full paths
    all_objects = cmds.ls(long=True)  # 'long=True' returns full DAG paths (e.g., "|group1|namespace:Iouri_Iouri")
    
    # Check if any object's full path ends with "Iouri_Iouri" or "IOURI_RIG"
    iouri_rig_found = any(obj.rsplit("|", 1)[-1] in {"Iouri_Iouri", "IOURI_Rig"} for obj in all_objects)
    
    if iouri_rig_found:
        print("Iouri Rig found! Proceeding with export.")
        # Object lists (without namespaces)
        fx_objects = ["gp_retopo_shoe_L", "gp_retopo_shoe_R", "msh_body_low3"]
        shd_objects = ["GP_inside_mouth_low", "gp_eye_elements", "gp_retopo_shoe_L",
                       "gp_retopo_shoe_R", "msh_body_low3", "msh_nails_low"]
        eyes_objects = ["gp_eye_elements"]

        # Export Iouri's assets
        if ExportIouri == True :
            export_abc(get_full_paths(fx_objects), "IOURI_FX", version_folder, scene_name, start_frame, end_frame)
            export_abc(get_full_paths(shd_objects), "IOURI_SHD", version_folder, scene_name, start_frame, end_frame)
            export_abc(get_full_paths(eyes_objects), "IOURI_EYES", version_folder, scene_name, start_frame, end_frame)
        else : 
            print("Iouri Export variable is set to false, ignoring Iouri for export")
    else:
        print("Iouri Rig not found. Skipping Iouri export.")
        
    # Check if Kat is in the scene
    if cmds.objExists("Kat_Katarina"):
        print("Kat Rig found! Proceeding with export.")

        # Object lists (without namespaces)
        kat_meshes = [
            "GRP_GEO_KAT"
        ]

        # Export Kat's assets
        if ExportKat == True :
            
            # Turn on Live Boolean
            
                        
            # Proceed to Export                                    
            export_abc(get_full_paths(kat_meshes), "KAT", version_folder, scene_name, start_frame, end_frame)
        else :
            print("ExportKat variable is set to False, ignoring Kat for export")
    else:
        print("Kat Rig not found. Skipping Kat export.")

    # Check if selection set "Ramses_Publish" exists and contains objects
    if cmds.objExists("Ramses_Publish"):
        props_objects = cmds.sets("Ramses_Publish", q=True) or []  # Get objects or empty list
               
        if props_objects:
            if ExportProps == True : 
                print(f"Exporting {len(props_objects)} objects from Ramses_Publish set.")
                export_abc(props_objects, "PROPS", version_folder, scene_name, start_frame, end_frame)
                
            else: 
                print("Props Export is set to False, ignoring props for export")
        else:
            print("Ramses_Publish set is empty. No PROPS export.")
    else:
        print("Ramses_Publish set not found. No PROPS export.")

    # Select and export cameras (from CAM and mirrored_ objects)
    selected_cameras = select_cameras()

    if selected_cameras:
        # Export the selected cameras as a .ma or .mb file (depending on the scene type)
        camera_filename = f"{base_name}_cameras.mb"
        camera_file_path = os.path.join(version_folder, camera_filename).replace("\\", "/")
        
        # Export cameras as .mb file
        if ExportCameras == True:
            cmds.file(camera_file_path, exportSelected=True, type="mayaBinary")
            print(f"Exported cameras to: {camera_file_path}")
        else: 
            print("Export camera is set to False, not exporting cameras")
    else:
        print("No cameras found to export.")


