import maya.cmds as cmds

def find_latest_shader(base_name):
    """
    Finds the latest version of a shader based on its base name.
    """
    shaders = cmds.ls(base_name + "*", materials=True)
    if not shaders:
        return None
    
    # Sort by last numerical character
    shaders.sort(key=lambda s: int(s[len(base_name):]) if s[len(base_name):].isdigit() else 0)
    return shaders[-1]  # Return the highest version

def assign_shaders():
    """
    Assign shaders to the correct shape nodes within the selection, including stand-ins.
    """
    shader_assignments = {
    
        "SHD_Shutter": [
            "MSH_Cable_inter_top", "Blades_result_msh", "Blade_mshShape", "Blade_mshShapeOrig", "Boolean_msh", "Blades_result_mshShape"
            ],
        "SHD_Kat": [
            "MSH_HeadShape", "MSH_BaseShape", "MSH_RailsShape", 
            "MSH_Head_CableShape", "MSH_Arm_RShape", "MSH_LegsShape", "MSH_Arm_LShape", "MSH_BustShape"
        ],
        "SHD_Cables": [
            "MSH_Cable_extShape", "MSH_Cable_inter_topShape", "MSH_Cable_inter_bottomShape"
        ],
        "SHD_BODY": [
            "msh_bttm_molar_02_RShape", "msh_top_molar_02_LShape", "msh_top_molar_01_LShape", "msh_top_premolar_01_LShape", 
            "msh_bttm_incisors_02_RShape", "msh_bttm_molar_01_RShape", "msh_bttm_premolar_02_RShape", "msh_bttm_premolar_01_RShape", 
            "msh_bttm_incisors_01_LShape", "msh_bttm_incisors_02_LShape", "msh_bttm_canine_RShape", "msh_bttm_incisors_01_RShape", 
            "msh_gumsShape", "msh_body_low3Shape", "msh_bttm_premolar_02_LShape", "msh_bttm_canine_LShape", "msh_bttm_premolar_01_LShape", 
            "msh_bttm_molar_01_LShape", "msh_caracunla_lowShape", "msh_nails_lowShape", "msh_bttm_molar_02_LShape", 
            "msh_tongue_lowint_boucheIOURIShape", "msh_top_molar_02_RShape", "msh_top_molar_01_RShape", "msh_top_premolar_02_RShape", 
            "msh_top_canine_RShape", "msh_top_premolar_01_RShape", "msh_top_incisors_02_RShape", "msh_top_incisors_01_RShape", 
            "msh_top_incisors_02_LShape", "msh_top_canine_LShape", "msh_top_incisors_01_LShape", "msh_top_premolar_02_LShape"
        ],
        "SHD_COMBI": [
            "cloth_shape_0", "Kamarade_A_IouriSuit_Mod_Iouri_A_pose_high_Thick_reparationShape"
        ],
        "SHD_HAIR": ["GROOM_Hair", "GROOM_Lashes", "GROOM_Brows"],
        "SHD_IRIS": ["msh_iris_lowShape"],
        "SHD_EYES_CORNEA": ["msh_meniscus_lowShape", "msh_cornea_lowShape"],
        "SHD_SHOES": [
            "msh_shoe_flap_LShape", "msh_coutures_shoes_RShape", "msh_coutures_shoes_LShape", "msh_shoe_base_body_LShape", 
            "msh_shoe_wave_fabric_LShape", "msh_shoes_hard_top_LShape", "msh_cube_back_shoe_LShape", "msh_shoe_sole_LShape", 
            "msh_shoe_flap_RShape", "msh_shoe_base_body_RShape", "msh_shoe_wave_fabric_RShape", "msh_shoes_hard_top_RShape", 
            "msh_shoe_sole_RShape", "msh_cube_back_shoes_RShape"
        ]
    }
    
    selected_objects = cmds.ls(selection=True, long=True)
    if not selected_objects:
        cmds.warning("No objects selected. Please select objects before running the script.")
        return
    
    # Select hierarchy to ensure all shapes and stand-ins are included
    cmds.select(selected_objects, hierarchy=True)
    selected_shapes = cmds.ls(selection=True, long=True, shapes=True) + cmds.ls(selection=True, long=True, type='aiStandIn')
    
    for base_shader, shape_list in shader_assignments.items():
        latest_shader = find_latest_shader(base_shader)
        if not latest_shader:
            cmds.warning(f"Shader '{base_shader}' not found.")
            continue
        
        shading_group = cmds.listConnections(latest_shader, type="shadingEngine")
        if not shading_group:
            cmds.warning(f"No shading group found for shader '{latest_shader}'.")
            continue
        
        shading_group = shading_group[0]
        
        for shape in shape_list:
            full_shape_path = [s for s in selected_shapes if shape in s]
            if full_shape_path:
                cmds.sets(full_shape_path, edit=True, forceElement=shading_group)
                print(f"Assigned {latest_shader} to {', '.join(full_shape_path)}")
            else:
                print(f"Shape '{shape}' not found in the selection, skipping.")

# Run the function
assign_shaders()
