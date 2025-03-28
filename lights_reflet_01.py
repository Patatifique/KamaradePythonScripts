import maya.cmds as cmds

def duplicate_light_group():
    original_group = "LGT"
    new_group = "LGT_Reflet"

    # Vérifier si "LGT" existe
    if not cmds.objExists(original_group):
        cmds.warning(f"Le groupe {original_group} n'existe pas.")
        return
    
    # Supprimer l'ancien "LGT_Reflet" s'il existe déjà
    if cmds.objExists(new_group):
        cmds.delete(new_group)

    # Dupliquer le groupe "LGT"
    duplicated_group = cmds.duplicate(original_group, name=new_group)[0]

    # Trouver tous les enfants du groupe "LGT_Reflet"
    children = cmds.listRelatives(duplicated_group, allDescendents=True, fullPath=True) or []

    # Supprimer les lights qui contiennent "Rim" ou "RIM" dans leur nom long
    for child in children:
        if "Rim" in child or "RIM" in child:
            cmds.delete(child)

    print(f"{new_group} créé avec succès, sans les lights 'Rim'.")

# Exécuter la fonction
duplicate_light_group()