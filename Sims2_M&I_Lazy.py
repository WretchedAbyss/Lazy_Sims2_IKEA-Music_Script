import os
import re
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory

def copy_files(source_folder, install_location):
    # Define paths relative to the source and destination
    files_to_copy = [
        {
            'source': os.path.join(source_folder, "University Life","EP1", "TSData", "Res", "Sound", "CollegeRock.package"),
            'dest': os.path.join(install_location, "EP1", "TSData", "Res", "Sound", "CollegeRock.package")
        },
        {
            'source': os.path.join(source_folder, "Best of Business","EP3", "TSData", "Res", "Sound", "NewWave.package"),
            'dest': os.path.join(install_location, "EP3", "TSData", "Res", "Sound", "NewWave.package")
        },
        {
            'source': os.path.join(source_folder, "Bon Voyage", "TSData", "Res", "Sound", "Reggae.package"),
            'dest': os.path.join(install_location, "EP6", "TSData", "Res", "Sound", "Reggae.package")
        },
        # New untested stuff
        {
            'source': os.path.join(source_folder, "Free Time", "TSData", "Res", "Sound", "Pop.package"),
            'dest': os.path.join(install_location, "EP7", "TSData", "Res", "Sound", "Pop.package")
        },
        {
            'source': os.path.join(source_folder, "Apartment Life", "TSData", "Res", "Sound", "CollegeRock.package"),
            'dest': os.path.join(install_location, "EP8", "TSData", "Res", "Sound", "CollegeRock.package")
        },
        {
            'source': os.path.join(source_folder, "Apartment Life", "TSData", "Res", "Sound", "Pop.package"),
            'dest': os.path.join(install_location, "EP8", "TSData", "Res", "Sound", "Pop.package")
        },
        {
            'source': os.path.join(source_folder, "Best of Business","SP5", "TSData", "Res", "Sound", "Pop.package"),
            'dest': os.path.join(install_location, "SP5", "TSData", "Res", "Sound", "Pop.package")
        },
        {
            'source': os.path.join(source_folder, "University Life","SP6", "TSData", "Res", "Sound", "Metal.package"),
            'dest': os.path.join(install_location, "SP6", "TSData", "Res", "Sound", "Metal.package")
        },
        {
            'source': os.path.join(source_folder, "Best of Business","SP7", "TSData", "Res", "Sound", "Salsa.package"),
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

def copy_sp8(source_folder, destination_folder):
    # Find SP8 in the source folder
    for root, dirs, files in os.walk(source_folder):
        if 'SP8' in dirs or 'SP8' in files:
            sp8_path = os.path.join(root, 'SP8')
            break
    else:
        raise FileNotFoundError("SP8 file or directory not found in the source folder.")

    # Destination path for SP8
    sp8_destination = os.path.join(destination_folder, "SP8")

    # If SP8 is a directory, use copytree; if it's a file, use copy2
    if os.path.isdir(sp8_path):
        # Ensure the destination directory for SP8 exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.copytree(sp8_path, sp8_destination)
    else:
        # Ensure the destination directory exists for the file
        if not os.path.exists(os.path.dirname(sp8_destination)):
            os.makedirs(os.path.dirname(sp8_destination))
        shutil.copy2(sp8_path, sp8_destination)

    print(f"Successfully copied SP8 to {destination_folder}")
# Example usage:
# copy_folder('/path/to/source/SP8', '/path/to/destination')

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
    source_folder = askdirectory(title="Select Source The Sims 2 Starter Pack:")
    
    if not source_folder:
        print("No source folder selected, operation cancelled.")
    else:
        # Ask for the game installation location for music files and SP8
        install_location = askdirectory(title="Select The Sims 2 Legacy Collection Install Location")
        
        if not install_location:
            print("No install location selected, operation cancelled.")
        else:
            copy_files(source_folder, install_location)
            copy_sp8(source_folder, install_location)
            amend_vdf_file(install_location)