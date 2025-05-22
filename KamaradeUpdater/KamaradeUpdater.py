import os
from pickle import FALSE
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading

# This script was written by Hubert Chauvaux on the 21st of may 2025 cause he was tired of copying files manually :)

##################################################################################
##################################################################################
########################## PLAYBLAST UPDATER #####################################
# This script scans a folder for playblast files, checks for the latest versions,
# and copies them to a new location if they are newer than the reference files.
##################################################################################
##################################################################################



# stuff to make it adaptable to other projects :)

ProjectShotsDirectory = fr"S:\SIC3D\SIC5\Projects\KAMARADE\05-SHOTS"

# Playblasts
EditPlayblastsDirectory = fr"Z:\sources images\KAMARADE\PlayBlasts"

# Rendu folders

# Project name as defined on the share like S:\SIC3D\SIC5\Projects\KAMARADE\05-SHOTS\Kamarade_S_SQ1-SH040\Kamarade_S_SQ1-SH040_Anim
ProjectName = "Kamarade_S_"
# Naming convention for folders that contain the exr (there's 2 in Kamarade)
# Ex: SQ2_SH100_RENDU_MAYA  SQ2_SH100_RENDU_COMP
RenduMayaSuffix = "_RENDU_MAYA"
RenduCompSuffix = "_RENDU_COMP"

# Base folder for Rendu
EditRenduDirectory = fr"Z:\sources images\KAMARADE"


# DEBUG STUFF

# I made this for testing, it creates empty folders in place of copying folders for RENDU, so it can test without the LONG time of copying EXR
# If you want to use it, set it to True
EMPTY_FOLDER_MODE = False

# If you want to copy folders with less frames, set it to True
COPY_FOLDERS_WITH_LESS_FRAMES = False


def scan_folder(folder_path):
    all_items = []
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            all_items.append(os.path.join(root, name))
    return all_items

def get_latest_shots(file_paths):
    latest_files = {}
    for path in file_paths:
        filename = os.path.basename(path)
        if "Anim" not in filename:
            continue
        
        # Base shot name: everything up to and including 'Anim'
        # e.g. "Shot123_Anim_v01.mp4" -> "Shot123_Anim"
        anim_index = filename.find("Anim") + len("Anim")
        name_part = filename[:anim_index]

        try:
            modified_time = os.path.getmtime(path)
        except FileNotFoundError:
            continue
        
        # Keep only the most recent file for this shot
        if name_part not in latest_files or modified_time > latest_files[name_part][1]:
            latest_files[name_part] = (path, modified_time)
    
    # Return dict with shot base name: full path of latest file
    return {name: data[0] for name, data in latest_files.items()}

def check_and_copy_newer_previews(latest_shots_dict):
    today = datetime.today().strftime("%d_%m_%y_%Hh%M")
    output_folder = fr"{EditPlayblastsDirectory}\{today}"
    os.makedirs(output_folder, exist_ok=True)

    margin_seconds = 10  # margin to prevent copying due to small timestamp differences

    for base_name, reference_file in latest_shots_dict.items():
        shot_folder_name = base_name.replace("_Anim", "")
        preview_dir = fr"{ProjectShotsDirectory}\{shot_folder_name}\{base_name}\_preview"

        if not os.path.exists(preview_dir):
            print(f"Preview folder not found for {base_name}")
            continue

        reference_time = os.path.getmtime(reference_file)

        preview_mp4s = [
            os.path.join(preview_dir, f)
            for f in os.listdir(preview_dir)
            if f.lower().endswith(".mp4") and os.path.isfile(os.path.join(preview_dir, f))
        ]

        if not preview_mp4s:
            print(f"No .mp4 files in preview for {base_name}")
            continue

        newest_preview = max(preview_mp4s, key=os.path.getmtime)
        newest_time = os.path.getmtime(newest_preview)

        if newest_time > (reference_time + margin_seconds):
            # debug stuff i don't actually print these anymore
            # print(f"Reference file: {reference_file}, mtime: {reference_time}")
            # print(f"Newest preview: {newest_preview}, mtime: {newest_time}")
            try:
                base_shot_name = os.path.basename(newest_preview).split("Anim")[0] + "Anim.mp4"
                destination_path = os.path.join(output_folder, base_shot_name)
                shutil.copy2(newest_preview, destination_path)
                print(f"Copied newer preview for {base_name}: {os.path.basename(newest_preview)}")
            except Exception as e:
                print(f"Failed to copy preview for {base_name}: {e}")
        else:
            print(f"Preview is not newer for {base_name}")

# Run function
def run_playblast_update():
    try:
        base_playblast_path = fr"{EditPlayblastsDirectory}"
        scanned_files = scan_folder(base_playblast_path)
        mp4_files = [f for f in scanned_files if f.lower().endswith(".mp4")]
        latest_shots = get_latest_shots(mp4_files)
        check_and_copy_newer_previews(latest_shots)
        
        messagebox.showinfo("Success", "Playblast update completed!")
        print ("Playblast update completed!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


##################################################################################
##################################################################################
########################## RENDU FOLDER UPDATER ##################################
##################################################################################
##################################################################################


def scan_for_rendu_folders(root_dir):
    rendu_folders = {}
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            if d.endswith(f"{RenduMayaSuffix}") or d.endswith(f"{RenduCompSuffix}"):
                full_path = os.path.join(root, d)
                shot_key = d  # Can be refined if needed
                mtime = os.path.getmtime(full_path)
                if shot_key not in rendu_folders or mtime > rendu_folders[shot_key][1]:
                    rendu_folders[shot_key] = (full_path, mtime)
    return rendu_folders

def get_corresponding_drive_folder(folder_name):
    # Ex: SQ2_SH100_RENDU_MAYA -> Kamarade_S_SQ2-SH100/Kamarade_S_SQ2-SH100_Comp
    parts = folder_name.split("_")
    if len(parts) < 3:
        return None

    sq, sh = parts[0], parts[1]
    shot_code = f"{sq}-{sh}"

    folder = f"{ProjectName}{shot_code}\\{ProjectName}{shot_code}_Comp"
    return os.path.join(fr"{ProjectShotsDirectory}", folder)

def count_frames_in_folder(folder_name):
    count = 0
    if not os.path.exists(folder_name):
        return 0

    for file in os.listdir(folder_name):
        if file.lower().endswith(".exr") and os.path.isfile(os.path.join(folder_name, file)):
            count += 1
    return count

def check_and_copy_rendu_folders(rendu_dict):
    today = datetime.today().strftime("EXPORT_%d_%m_%y_%Hh%M")
    output_folder = os.path.join(fr"{EditRenduDirectory}", today)
    os.makedirs(output_folder, exist_ok=True)
    margin_seconds = 10  # margin to prevent copying due to small timestamp differences

    for folder_name, (rendu_path, rendu_mtime) in rendu_dict.items():
        s_drive_path_Base = get_corresponding_drive_folder(folder_name)
        s_drive_path = fr"{s_drive_path_Base}\{folder_name}"
        if not s_drive_path or not os.path.exists(s_drive_path):
            print(f"Corresponding drive folder not found: {folder_name}")
            continue

        s_drive_mtime = os.path.getmtime(s_drive_path)
        if s_drive_mtime > (rendu_mtime + margin_seconds):
            # debug stuff i don't actually print these anymore
            # print(f"RENDU folder: {rendu_path}, mtime: {rendu_mtime}")
            # print(f"Corresponding folder: {s_drive_path}, mtime: {s_drive_mtime}")

            # compare frames
            s_driveFolderFrameCount = count_frames_in_folder(s_drive_path)
            montageFolderFrameCount = count_frames_in_folder(rendu_path)
            
            # debug, unused for now
            # print(f"{s_driveFolderFrameCount}, {montageFolderFrameCount}")
            if s_driveFolderFrameCount < montageFolderFrameCount:
                if COPY_FOLDERS_WITH_LESS_FRAMES == False:
                    print(f"Corresponding drive folder has less frames: {folder_name}, not copying. Expected: {montageFolderFrameCount}, Current:{s_driveFolderFrameCount}")
                    continue
                else:
                    print(f"Corresponding drive folder has less frames: {folder_name}, copying anyway.  Expected: {montageFolderFrameCount}, Current:{s_driveFolderFrameCount}")

            try:
                if EMPTY_FOLDER_MODE == False:
                    # create the folder
                    destination_folder_path = os.path.join(output_folder, folder_name)
                    original_folder_path = s_drive_path
                    print(f"Copying {folder_name}..... (this might take a while)")
                    shutil.copytree(original_folder_path, destination_folder_path)
                    print(f"Copied newer folder for {folder_name}")
                else:
                    # create an empty folder for testing
                    destination_folder_path = os.path.join(output_folder, folder_name)
                    os.makedirs(destination_folder_path, exist_ok=True)
                    print(f"Created empty folder for {folder_name}")
            except Exception as e:
                print(f"Failed to create folder for {folder_name}: {e}")
        else:
            print(f"RENDU folder is not updated: {folder_name}")

# Run function
def run_rendu_update():
    try:
        base_folder = fr"{EditRenduDirectory}"
        rendu_folders = scan_for_rendu_folders(base_folder)
        check_and_copy_rendu_folders(rendu_folders)
        messagebox.showinfo("Success", "RENDU folder update completed!")
        print("RENDU folder update completed!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")








#######################################################################
#######################################################################
########################## GUI Setup ##################################
#######################################################################
#######################################################################

root = tk.Tk()
root.title("Kamarade Shot Updater")
root.geometry("300x150")

def on_playblast_click():
    threading.Thread(target=run_playblast_update).start()

def on_rendu_click():
    threading.Thread(target=run_rendu_update).start()

tk.Button(root, text="Run Playblast Update", command=on_playblast_click, height=2, width=25).pack(pady=10)
tk.Button(root, text="Run Rendered Shots Update", command=on_rendu_click, height=2, width=25).pack(pady=10)

root.mainloop()
