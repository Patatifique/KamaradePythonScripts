import maya.cmds as cmds
import maya.mel as mel
import json


# Script used to setup iouri anim before export to marvelous and houdini

#def to get objects with namespace
def find_object_with_namespace(base_name):
    objects = cmds.ls(f"*:{base_name}") or cmds.ls(base_name)
    if not objects:
        raise ValueError(f"Object '{base_name}' isn't found")
    return objects[0]

def select_iouri_controllers():
    """Selects Iouri's controllers."""
    controllers = [
        "COG_ctl", "FLY", "TRAJ", "WORLD", "ankle_L_IK_ctl", "ankle_R_IK_ctl", "armMid_L_ctl", "armMid_R_ctl", "arm_L_IK_ctl", 
        "arm_L_PV_ctl", "arm_L_ctl", "arm_L_options_ctl", "arm_L_pin_ctrl", "arm_L_tweaker01_ctl", "arm_L_tweaker02_ctl", 
        "arm_L_tweaker03_ctl", "arm_L_tweaker04_ctl", "arm_R_IK_ctl", "arm_R_PV_ctl", "arm_R_ctl", "arm_R_options_ctl", 
        "arm_R_pin_ctrl", "arm_R_tweaker01_ctl", "arm_R_tweaker02_ctl", "arm_R_tweaker03_ctl", "arm_R_tweaker04_ctl", 
        "bottomSpine_IK_ctl", "breath_ctl", "button_L0_ctl", "button_L1_ctl", "button_R0_ctl", "button_R1_ctl", "cheek_L0_ctl", 
        "cheek_L1_ctl", "cheek_L2_ctl", "cheek_L3_ctl", "cheek_L_main_ctl", "cheek_R0_ctl", "cheek_R1_ctl", "cheek_R2_ctl", 
        "cheek_R3_ctl", "cheek_R_main_ctl", "clav_L_ctl", "clav_R_ctl", "collar_C0_ctl", "collar_C1_ctl", "collar_L0_ctl", 
        "collar_L1_ctl", "collar_L2_ctl", "collar_R0_ctl", "collar_R1_ctl", "collar_R2_ctl", "collar_orient_L_ctl", 
        "collar_orient_R_ctl", "collar_orient_back_ctl", "collar_orient_front_ctl", "ear_L_ctl", "ear_R_ctl", "elbow_L_ctl", 
        "elbow_R_ctl", "eye_L00_ctl", "eye_L_L_ctl", "eye_R00_ctl", "eye_R_L_ctl", "eyebrow_L_ctl", "eyebrow_R_ctl", 
        "eyebrow_xtra_L0_ctl", "eyebrow_xtra_L1_ctl", "eyebrow_xtra_L2_ctl", "eyebrow_xtra_L3_ctl", "eyebrow_xtra_R0_ctl", 
        "eyebrow_xtra_R1_ctl", "eyebrow_xtra_R2_ctl", "eyebrow_xtra_R3_ctl", "foot_L_ctl", "foot_R_ctl", "forearmMid_L_ctl", 
        "forearmMid_R_ctl", "forearm_L_ctl", "forearm_L_tweaker01_ctl", "forearm_L_tweaker02_ctl", "forearm_L_tweaker03_ctl", 
        "forearm_L_tweaker04_ctl", "forearm_R_ctl", "forearm_R_tweaker01_ctl", "forearm_R_tweaker02_ctl", "forearm_R_tweaker03_ctl", 
        "forearm_R_tweaker04_ctl", "frown_ctl", "hand_L_IK_ctl", "hand_R_IK_ctl", "head_ctl", "head_option_ctl", "hip_L_IK_ctl", 
        "hip_R_IK_ctl", "hips_IK_ctl", "hips_L_ctl", "hips_R_ctl", "jaw_C0_ctl", "jaw_rotate_ctl", "kneeMid_L_ctl", "kneeMid_R_ctl", 
        "knee_L_ctl", "knee_L_tweaker01_ctl", "knee_L_tweaker02_ctl", "knee_L_tweaker03_ctl", "knee_L_tweaker04_ctl", "knee_R_ctl", 
        "knee_R_tweaker01_ctl", "knee_R_tweaker02_ctl", "knee_R_tweaker03_ctl", "knee_R_tweaker04_ctl", "knee_ribbon_L_ctl", 
        "knee_ribbon_R_ctl", "legMid_L_ctl", "legMid_R_ctl", "leg_L_PV_ctl", "leg_L_options_ctl", "leg_L_pin_ctrl", 
        "leg_L_tweaker01_ctl", "leg_L_tweaker02_ctl", "leg_L_tweaker03_ctl", "leg_L_tweaker04_ctl", "leg_R_PV_ctl", 
        "leg_R_options_ctl", "leg_R_pin_ctrl", "leg_R_tweaker01_ctl", "leg_R_tweaker02_ctl", "leg_R_tweaker03_ctl", 
        "leg_R_tweaker04_ctl", "lids_down_L0_ctl", "lids_down_L1_ctl", "lids_down_L2_ctl", "lids_down_R0_ctl", 
        "lids_down_R1_ctl", "lids_down_R2_ctl", "lids_down_main_L0_ctl", "lids_down_main_R0_ctl", "lids_side_L0_ctl", 
        "lids_side_L1_ctl", "lids_side_R0_ctl", "lids_side_R_ctl", "lids_up_L0_ctl", "lids_up_L1_ctl", "lids_up_L2_ctl", "lids_up_R0_ctl", 
        "lids_up_R1_ctl", "lids_up_R2_ctl", "lids_up_main_L0_ctl", "lids_up_main_R0_ctl", "lip_down_C0_ctl", "lip_down_L0_ctl", 
        "lip_down_R0_ctl", "lip_side_L0_ctl", "lip_side_R0_ctl", "lip_up_C0_ctl", "lip_up_L0_ctl", "lip_up_R0_ctl", "lookAt_L_ctl", 
        "lookAt_R_ctl", "lookAt_ctl", "lower_lip_ctrl", "lowerteeth_ctl", "meta_L_ctl", "meta_R_ctl", "metamiddle_L_ctl", 
        "metamiddle_R_ctl", "metapinky_L_ctl", "metapinky_R_ctl", "metapointer_L_ctl", "metapointer_R_ctl", "metaring_L_ctl", 
        "metaring_R_ctl", "midSpine_IK_ctl", "midSpine_ctl", "middle_01_L_ctl", "middle_01_R_ctl", "middle_02_L_ctl", 
        "middle_02_R_ctl", "middle_03_L_ctl", "middle_03_R_ctl", "middle_L_IK_ctl", "middle_L_IK_pivot_ctl", "middle_L_pv_ctl", 
        "middle_R_IK_ctl", "middle_R_IK_pivot_ctl", "middle_R_pv_ctl", "middle_base_L_ctl", "middle_base_R_ctl", "mouth_L_ctl", 
        "mouth_R_ctl", "mouth_ctrl", "neck_01_ctl", "neck_02_ctl", "neck_03_ctl", "nose_ctl", "nostril_L_ctl", "nostril_R_ctl", 
        "pinky_01_L_ctl", "pinky_01_R_ctl", "pinky_02_L_ctl", "pinky_02_R_ctl", "pinky_03_L_ctl", "pinky_03_R_ctl", "pinky_L_IK_ctl", 
        "pinky_L_IK_pivot_ctrl", "pinky_L_pv_ctl", "pinky_R_IK_ctl", "pinky_R_IK_pivot_ctrl", "pinky_R_pv_ctl", "pinky_base_L_ctl", 
        "pinky_base_R_ctl", "pointer_01_L_ctl", "pointer_01_R_ctl", "pointer_02_L_ctl", "pointer_02_R_ctl", "pointer_03_L_ctl", 
        "pointer_03_R_ctl", "pointer_L_IK_ctl", "pointer_L_IK_pivot_ctl", "pointer_L_pv_ctl", "pointer_R_IK_ctl", 
        "pointer_R_IK_pivot_ctl", "pointer_R_pv_ctl", "pointer_base_L_ctl", "pointer_base_R_ctl", "ring_01_L_ctl", 
        "ring_01_R_ctl", "ring_02_L_ctl", "ring_02_R_ctl", "ring_03_L_ctl", "ring_03_R_ctl", "ring_L_IK_ctl", "ring_L_IK_pivot_ctrl", "ring_L_pv_ctl", 
        "ring_R_IK_ctl", "ring_R_IK_pivot_ctrl", "ring_R_pv_ctl", "ring_base_L_ctl", "ring_base_R_ctl", "spine_L_options_ctl", "spine_tweak_01_ctl", 
        "spine_tweak_02_ctl", "spine_tweak_03_ctl", "spine_tweak_04_ctl", "spine_tweak_05_ctl", "throat_ctl", "thumb_01_L_ctl", "thumb_01_R_ctl", 
        "thumb_02_L_ctl", "thumb_02_R_ctl", "thumb_03_L_ctl", "thumb_03_R_ctl", "thumb_L_IK_ctl", "thumb_L_IK_pivot_ctl", "thumb_L_pv_ctl", "thumb_R_IK_ctl", 
        "thumb_R_IK_pivot_ctl", "thumb_R_pv_ctl", "thumb_base_L_ctl", "thumb_base_R_ctl", "toes_L_ctl", "toes_R_ctl", "tongue_01_ctl", "tongue_02_ctl", 
        "tongue_03_ctl", "tongue_04_ctl", "tongue_05_ctl", "topSpine_IK_ctl", "topSpine_ctl", "upper_lip_ctrl", "upperteeth_ctl", "wrist_L_ctl", "wrist_R_ctl"

    ]
    
    selected_controls = []
    iouri_children = cmds.listRelatives("Iouri_Iouri", allDescendents=True, fullPath=True) or []   
    
    for ctrl in controllers:
        # Find all possible matches for this controller name
        all_matches = cmds.ls(f"*:{ctrl}") or cmds.ls(ctrl)
        
        # Find the first match that's in Iouri's hierarchy
        for match in all_matches:
            full_path = cmds.ls(match, long=True)[0]
            if full_path in iouri_children:
                selected_controls.append(match)
                break
    
    if selected_controls:
        cmds.select(selected_controls, replace=True)
        print(f"Selected Iouri's controllers: {selected_controls}")
    else:
        cmds.warning("No Iouri controllers found in the scene.")


# Run selection function before baking
select_iouri_controllers()


def switch_to_ik(side):
    try:
        # Get Objects with right side and namespaces
        arm_options_ctl = find_object_with_namespace(f"arm_{side}_options_ctl")
        arm_ctl = find_object_with_namespace(f"arm_{side}_ctl")
        arm_ik = find_object_with_namespace(f"arm_{side}_ik")
        elbow_ctl = find_object_with_namespace(f"elbow_{side}_ctl")
        elbow_ik = find_object_with_namespace(f"elbow_{side}_ik")
        wrist_ctl = find_object_with_namespace(f"wrist_{side}_ctl")
        wrist_ik = find_object_with_namespace(f"wrist_{side}_ik")
        arm_ik_ctl = find_object_with_namespace(f"arm_{side}_IK_ctl")
        arm_pv_ctl = find_object_with_namespace(f"arm_{side}_PV_ctl")
        hand_ik_ctl = find_object_with_namespace(f"hand_{side}_IK_ctl")
        wrist_ik_loc = find_object_with_namespace(f"wrist_{side}_ik_loc")
    except ValueError as e:
        cmds.error(str(e))


    # Switch from FK to IK
    cmds.matchTransform(arm_ik_ctl, arm_ctl)
    cmds.matchTransform(arm_pv_ctl, elbow_ctl)
    cmds.matchTransform(hand_ik_ctl, wrist_ik_loc)

    # Do the Switch IK
    cmds.setAttr(f"{arm_options_ctl}.SwitchIK", 1)


def load_pose(file_path):
    """Loads a pose from a JSON file and applies it to the corresponding controls, Iouri specific"""
    try:
        with open(file_path, "r") as jsonFile:
            pose_data = json.load(jsonFile)
        
        # Get Iouri's hierarchy once (with full paths)
        iouri_children = cmds.listRelatives("Iouri_Iouri", allDescendents=True, fullPath=True) or []
        
        for ctrl, attrs in pose_data.items():
            # Find all possible matches for this controller name
            all_matches = cmds.ls(f"*:{ctrl}") or cmds.ls(ctrl)
            
            # Find the first match that's in Iouri's hierarchy
            target_ctrl = None
            for match in all_matches:
                full_path = cmds.ls(match, long=True)[0]
                if full_path in iouri_children:
                    target_ctrl = match
                    break
            
            if target_ctrl:  # Only proceed if we found the correct controller
                for attr, value in attrs.items():
                    try:
                        cmds.setAttr(f"{target_ctrl}.{attr}", value)
                    except Exception as e:
                        print(f"Could not set {target_ctrl}.{attr}: {e}")
            else:
                print(f"Control {ctrl} not found in Iouri's hierarchy")
        
        print(f"Pose loaded successfully from {file_path}")
    except Exception as e:
        print(f"Failed to load pose: {e}")


def bake_selected_animation():
    # Get the currently selected objects
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("No objects selected. Please select objects to bake.")
        return

    # Set bakeResults options (you can adjust these to your needs)
    cmds.bakeResults(selected_objects,
                     time=(cmds.playbackOptions(q=True, min=True), cmds.playbackOptions(q=True, max=True)),
                     sampleBy=1,  # Adjust sample rate, 1 means every frame
                     preserveOutsideKeys=True,
                     simulation=True)  # Use the simulation flag
    
    print("Baking complete for selected objects.")
    
    # Get all animation layers
    anim_layers = cmds.ls(type='animLayer')
    
    if anim_layers and len(anim_layers) > 1:
        for obj in selected_objects:
            # Find animation layers connected to the object's animation curves
            anim_curves = cmds.listConnections(obj, type="animCurve") or []
            affected_layers = set()
    
            for curve in anim_curves:
                layers = cmds.listConnections(curve, type="animLayer") or []
                affected_layers.update(layers)
    
            # Skip if no animation layers are found
            if not affected_layers:
                continue
    
            # Remove animation layers except 'BaseAnimation'
            for layer in affected_layers:
                if layer != "BaseAnimation":
                    try:
                        cmds.setAttr(f"{layer}.lock", False)
                        mel.eval(f'delete {layer}')
                    except Exception as e:
                        cmds.warning(f"Failed to delete layer {layer}: {str(e)}")
                    
    # Delete Every Frame out of range! 
    start_frame = cmds.playbackOptions(q=True, min=True)
    end_frame = cmds.playbackOptions(q=True, max=True)
    
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected. Please select objects with animation.")
        return
    
    for obj in selected_objects:
        anim_curves = cmds.listConnections(obj, type='animCurve') or []
        for curve in anim_curves:
            key_times = cmds.keyframe(curve, query=True, timeChange=True) or []
            for key_time in key_times:
                if key_time < start_frame or key_time > end_frame:
                    cmds.cutKey(curve, time=(key_time, key_time))

    # Initialize flag to track completion of the operation
    operation_completed = False
    
    # Key the first frame and copy to a frame 25 frames before
    for obj in selected_objects:
        # Get all keyed frames for the object
        keyed_frames = cmds.keyframe(obj, q=True, timeChange=True)
        
        if not keyed_frames:
            cmds.warning(f"No keyframes found for {obj}.")
            continue
        
        # Get the first keyed frame (smallest time value)
        first_key_frame = min(keyed_frames)
        
        
        # Now copy and paste to 25 frames earlier
        new_frame = first_key_frame - 25
        if new_frame < 1:  # Avoid negative or zero frames
            new_frame = 1
        
        # Copy keyframes to the new frame (fixing the 'time' argument)
        cmds.copyKey(obj, time=(first_key_frame, first_key_frame))
        cmds.pasteKey(obj, time=(new_frame, new_frame))
        
        # Indicate that the operation was completed for this object
        operation_completed = True
    
    # Calculate the pose application frame (100 frames before the first keyframe)
    pose_apply_frame = first_key_frame - 100
    if pose_apply_frame < 1:
       pose_apply_frame = 1

    # Set the current frame to the first frame
    cmds.currentTime(first_key_frame)
 
    #Store every value needed to fix the cloth bind pose to fit first keyframe pose IK and parent spaces   
    arm_L_options_ctl = find_object_with_namespace("arm_L_options_ctl")
    arm_R_options_ctl = find_object_with_namespace("arm_R_options_ctl")
    
    switch_ik_value_L = cmds.getAttr(f"{arm_L_options_ctl}.SwitchIK")
    switch_ik_value_R = cmds.getAttr(f"{arm_R_options_ctl}.SwitchIK")
    
    arm_L_ctl = find_object_with_namespace("arm_L_ctl")
    arm_R_ctl = find_object_with_namespace("arm_R_ctl")

    arm_L_orient_space = cmds.getAttr(f"{arm_L_ctl}.OrientSpace")
    arm_R_orient_space = cmds.getAttr(f"{arm_R_ctl}.OrientSpace")

    arm_L_PV_ctl = find_object_with_namespace("arm_L_PV_ctl")
    arm_R_PV_ctl = find_object_with_namespace("arm_R_PV_ctl")

    arm_L_PV_parent_space = cmds.getAttr(f"{arm_L_PV_ctl}.ParentSpace")
    arm_R_PV_parent_space = cmds.getAttr(f"{arm_R_PV_ctl}.ParentSpace")

    hand_L_IK_ctl = find_object_with_namespace("hand_L_IK_ctl")
    hand_R_IK_ctl = find_object_with_namespace("hand_R_IK_ctl")

    hand_L_IK_parent_space = cmds.getAttr(f"{hand_L_IK_ctl}.ParentSpace")
    hand_R_IK_parent_space = cmds.getAttr(f"{hand_R_IK_ctl}.ParentSpace")

    leg_L_PV_ctl = find_object_with_namespace("leg_L_PV_ctl")
    leg_R_PV_ctl = find_object_with_namespace("leg_R_PV_ctl")

    leg_L_PV_parent_space = cmds.getAttr(f"{leg_L_PV_ctl}.ParentSpace")
    leg_R_PV_parent_space = cmds.getAttr(f"{leg_R_PV_ctl}.ParentSpace")

    ankle_L_IK_ctl = find_object_with_namespace("ankle_L_IK_ctl")
    ankle_R_IK_ctl = find_object_with_namespace("ankle_R_IK_ctl")

    ankle_L_IK_parent_space = cmds.getAttr(f"{ankle_L_IK_ctl}.ParentSpace")
    ankle_R_IK_parent_space = cmds.getAttr(f"{ankle_R_IK_ctl}.ParentSpace")
    

    
    # Set the current frame to the calculated pose application frame
    cmds.currentTime(pose_apply_frame)

    # Load the pose 100 frames before the first keyed frame
    pose_file_path = "S:\\SIC3D\\SIC5\\Projects\\KAMARADE\\02-PROD\\SCRIPTS\\Hubert\\ClothPose.json"  # Adjust path to the pose file
    load_pose(pose_file_path)

    # Apply the Switcher Code 
    if switch_ik_value_L == 1.0:
        switch_to_ik("L")
        # Filter if switched
        cmds.filterCurve(hand_L_IK_ctl, startTime=pose_apply_frame, endTime=first_key_frame, filter='euler')

    if switch_ik_value_R == 1.0:
        switch_to_ik("R")
        # Filter if switched
        cmds.filterCurve(hand_R_IK_ctl, startTime=pose_apply_frame, endTime=first_key_frame, filter='euler')
    
    # Change attributes based on the other stored values
    cmds.setAttr(f"{arm_L_ctl}.OrientSpace", arm_L_orient_space)
    cmds.setAttr(f"{arm_R_ctl}.OrientSpace", arm_R_orient_space)

    cmds.setAttr(f"{arm_L_PV_ctl}.ParentSpace", arm_L_PV_parent_space)
    cmds.setAttr(f"{arm_R_PV_ctl}.ParentSpace", arm_R_PV_parent_space)

    cmds.setAttr(f"{hand_L_IK_ctl}.ParentSpace", hand_L_IK_parent_space)
    cmds.setAttr(f"{hand_R_IK_ctl}.ParentSpace", hand_R_IK_parent_space)

    cmds.setAttr(f"{leg_L_PV_ctl}.ParentSpace", leg_L_PV_parent_space)
    cmds.setAttr(f"{leg_R_PV_ctl}.ParentSpace", leg_R_PV_parent_space)

    cmds.setAttr(f"{ankle_L_IK_ctl}.ParentSpace", ankle_L_IK_parent_space)
    cmds.setAttr(f"{ankle_R_IK_ctl}.ParentSpace", ankle_R_IK_parent_space)
    
    
    # Set keyframes for every attribute at the pose application frame
    for obj in selected_objects:
        attrs = cmds.listAttr(obj, k=True)  # Get all keyed attributes
        for attr in attrs:
            try:
                cmds.setKeyframe(obj, time=pose_apply_frame, attribute=attr)
            except Exception as e:
                cmds.warning(f"Failed to key {obj}.{attr}: {str(e)}")

    # Set all keyframes to linear interpolation
    for obj in selected_objects:
        cmds.keyTangent(obj, inTangentType="linear", outTangentType="linear")
    
    if operation_completed:
        print("Keyframe operations (keying, pasting, applying pose, and linear tangents) completed for all selected objects.")

# Run the bake function
bake_selected_animation()