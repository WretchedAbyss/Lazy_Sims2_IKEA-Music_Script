import os
import re
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory

def copy_files(source_folder, install_location):
    # Define paths relative to the source and destination
    files_to_copy = [
        {
            'source': os.path.join(source_folder, "The Sims 2 University", "TSData", "Res", "Sound", "CollegeRock.package"),
            'dest': os.path.join(install_location, "EP1", "TSData", "Res", "Sound", "CollegeRock.package")
        },
        {
            'source': os.path.join(source_folder, "The Sims 2 Open For Business", "TSData", "Res", "Sound", "NewWave.package"),
            'dest': os.path.join(install_location, "EP3", "TSData", "Res", "Sound", "NewWave.package")
        },
        {
            'source': os.path.join(source_folder, "The Sims 2 Bon Voyage", "TSData", "Res", "Sound", "Reggae.package"),
            'dest': os.path.join(install_location, "EP6", "TSData", "Res", "Sound", "Reggae.package")
        },
        # New untested stuff
        {
            'source': os.path.join(source_folder, "The Sims 2 FreeTime", "TSData", "Res", "Sound", "Pop.package"),
            'dest': os.path.join(install_location, "EP7", "TSData", "Res", "Sound", "Pop.package")
        },
        {
            'source': os.path.join(source_folder, "The Sims 2 Apartment Life", "TSData", "Res", "Sound", "CollegeRock.package"),
            'dest': os.path.join(install_location, "EP8", "TSData", "Res", "Sound", "CollegeRock.package")
        },
        {
            'source': os.path.join(source_folder, "The Sims 2 Apartment Life", "TSData", "Res", "Sound", "Pop.package"),
            'dest': os.path.join(install_location, "EP8", "TSData", "Res", "Sound", "Pop.package")
        },
        {
            'source': os.path.join(source_folder, "The Sims 2 H&M® Fashion Stuff", "TSData", "Res", "Sound", "Pop.package"),
            'dest': os.path.join(install_location, "SP5", "TSData", "Res", "Sound", "Pop.package")
        },
        {
            'source': os.path.join(source_folder, "The Sims 2 Teen Style Stuff", "TSData", "Res", "Sound", "Metal.package"),
            'dest': os.path.join(install_location, "SP6", "TSData", "Res", "Sound", "Metal.package")
        },
        {
            'source': os.path.join(source_folder, "The Sims 2 Kitchen & Bath Interior Design Stuff", "TSData", "Res", "Sound", "Salsa.package"),
            'dest': os.path.join(install_location, "SP7", "TSData", "Res", "Sound", "Salsa.package")
        }
    ]

    # Ensure the destination directories exist
    for file_info in files_to_copy:
        dest_dir = os.path.dirname(file_info['dest'])
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

    # Copy the files
    for file_info in files_to_copy:
        try:
            shutil.copy2(file_info['source'], file_info['dest'])
            print(f"Copied {file_info['source']} to {file_info['dest']}")
        except IOError as e:
            print(f"Unable to copy {file_info['source']}. Error: {e}")
        except Exception as e:
            print(f"Unexpected error occurred while copying {file_info['source']}. Error: {e}")

def copy_and_merge_folders(source_folder, install_location):
    # Paths for IKEA folders within the source folder
    ikea_original = os.path.join(source_folder, "The Sims 2 IKEA® Home Stuff")
    ikea_fix = os.path.join(source_folder, "The Sims 2 IKEA Home Stuff TS2 UC FIX")
    sp8_folder = os.path.join(install_location, "SP8")

    # Ensure the SP8 folder exists
    if not os.path.exists(sp8_folder):
        os.makedirs(sp8_folder)
    
    # First, copy contents of "The Sims 2 IKEA® Home Stuff"
    for root, _, files in os.walk(ikea_original):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, ikea_original)
            dest_path = os.path.join(sp8_folder, relative_path)
            
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            
            shutil.copy2(source_path, dest_path)

    # Then, copy contents of "The Sims 2 IKEA Home Stuff TS2 UC FIX", overwriting any duplicates
    for root, _, files in os.walk(ikea_fix):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, ikea_fix)
            dest_path = os.path.join(sp8_folder, relative_path)
            
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            
            shutil.copy2(source_path, dest_path)

def amend_vdf_file(install_location):
    vdf_file_path = os.path.join(install_location, "3314070_install.vdf")
    
    if not os.path.exists(vdf_file_path):
        print(f"VDF file not found at {vdf_file_path}")
        return

    new_entry = '''\t\t"HKEY_CURRENT_USER\\Software\\Electronic Arts\\The Sims 2 Ultimate Collection 25\\Sims2SP8.exe"
\t\t{
\t\t\t"string"
\t\t\t{
\t\t\t\t"path"		"%INSTALLDIR%\\SP8"
\t\t\t}
\t\t\t"dword"
\t\t\t{
\t\t\t\t"Installed"		"1"
\t\t\t}
\t\t}
'''

    with open(vdf_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Very broad search for Sims2SP7.exe
    sp7_block = re.search(r'(?=Sims2SP7\.exe).*?(?=\n\s*}|\Z)', content, re.DOTALL | re.IGNORECASE)
    
    if sp7_block:
        insert_point = sp7_block.end()
        # Look for three closing braces after this point
        remaining_content = content[insert_point:]
        brace_count = 0
        for i, char in enumerate(remaining_content):
            if char == '}':
                brace_count += 1
                if brace_count == 3:
                    insert_point += i + 1
                    break
        
        new_content = content[:insert_point] + '\n' + new_entry + content[insert_point:]
        
        # Update EPsInstalled
        ep_installed_match = re.search(r'(?m)\s*"EPsInstalled"\s*"\s*([^"]*)', new_content)
        if ep_installed_match:
            current_eps = ep_installed_match.group(1)
            if 'Sims2SP8.exe' not in current_eps:
                new_eps = current_eps + ',Sims2SP8.exe' if current_eps else 'Sims2SP8.exe'
                new_content = new_content.replace(current_eps, new_eps)
        
        with open(vdf_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print("VDF file has been updated with the new entry after Sims2SP7.exe.")
    else:
        print("Could not find 'Sims2SP7.exe' entry to insert after. Entry not added.")

if __name__ == "__main__":
    # Hide the main window
    Tk().withdraw() 

    # Ask for the source folder for Music Files
    source_folder = askdirectory(title="Select Source The Sims 2: Ultimate Collection")
    
    if not source_folder:
        print("No source folder selected, operation cancelled.")
    else:
        # Ask for the game installation location for music files and SP8
        install_location = askdirectory(title="Select The Sims 2 Legacy Collection Install Location")
        
        if not install_location:
            print("No install location selected, operation cancelled.")
        else:
            copy_files(source_folder, install_location)
            copy_and_merge_folders(source_folder, install_location)
            amend_vdf_file(install_location)