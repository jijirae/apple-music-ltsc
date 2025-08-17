import os
import zipfile
import shutil
import re
import subprocess
import sys

def select_msixbundle():
    folder = os.path.dirname(os.path.abspath(__file__))
    bundles = [f for f in os.listdir(folder) if f.endswith(".Msixbundle")]
    if not bundles:
        print("No .Msixbundle files found in this folder.")
        sys.exit(1)
    print("Apple Music Installer Script for Windows 10 versions 10.0.19044.0")
    print("Select a .Msixbundle file:")
    for i, bundle in enumerate(bundles, 1):
        print(f"{i}. {bundle}")

    while True:
        try:
            choice = int(input("Enter number: "))
            if 1 <= choice <= len(bundles):
                return os.path.join(folder, bundles[choice - 1])
            print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a number.")

def extract_zip(zip_path, extract_to):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)

if __name__ == "__main__":
    # Step 1: Select .Msixbundle in current folder
    selected_file = select_msixbundle()
    base, _ = os.path.splitext(selected_file)

    # Step 2: Rename .Msixbundle -> .zip (keep for later use)
    bundle_zip = base + ".zip"
    if os.path.exists(bundle_zip):
        print(f"Warning: {bundle_zip} already exists, overwriting.")
        os.remove(bundle_zip)
    os.rename(selected_file, bundle_zip)
    print(f"Renamed bundle to: {bundle_zip}")

    # Step 3: Extract bundle zip
    bundle_extract_dir = base + "_extracted"
    extract_zip(bundle_zip, bundle_extract_dir)
    print(f"Extracted bundle to: {bundle_extract_dir}")

    # Step 4: Find FIRST .msix in the extracted bundle (top-level only)
    msix_file = None
    for name in os.listdir(bundle_extract_dir):
        if name.endswith(".msix") or name.endswith(".Msix"):
            msix_file = os.path.join(bundle_extract_dir, name)
            break

    if not msix_file:
        print("No .msix file found inside the extracted bundle.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    print(f"Found msix: {msix_file}")

    # Step 5: Rename .msix -> .zip (keep for later use)
    msix_base, _ = os.path.splitext(msix_file)
    msix_zip = msix_base + ".zip"
    if os.path.exists(msix_zip):
        print(f"Warning: {msix_zip} already exists, overwriting.")
        os.remove(msix_zip)
    os.rename(msix_file, msix_zip)
    print(f"Renamed msix to: {msix_zip}")

    # Step 6: Extract msix zip
    msix_extract_dir = msix_base + "_extracted"
    extract_zip(msix_zip, msix_extract_dir)
    print(f"Extracted msix to: {msix_extract_dir}")

    # Step 7: Patch AppxManifest.xml (change ANY MinVersion to 10.0.19044.0)
    manifest_path = os.path.join(msix_extract_dir, "AppxManifest.xml")
    if not os.path.exists(manifest_path):
        print("AppxManifest.xml not found. Cannot patch.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(r'MinVersion="[^"]+"', 'MinVersion="10.0.19044.0"', content)
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated MinVersion in AppxManifest.xml to 10.0.19044.0")

    # Step 8: Remove specified files/folders
    targets = [
        os.path.join(msix_extract_dir, "AppxMetadata"),
        os.path.join(msix_extract_dir, "AppxSignature.p7x"),
        os.path.join(msix_extract_dir, "[Content_Types].xml"),
    ]
    for t in targets:
        if os.path.isdir(t):
            shutil.rmtree(t, ignore_errors=True)
            print(f"Removed folder: {t}")
        elif os.path.isfile(t):
            os.remove(t)
            print(f"Removed file: {t}")

    # Step 9: Show Developer Mode instructions first
    print("\nBefore proceeding, please enable Developer Mode:")
    print("Go to: Settings -> Windows Update -> For Developers -> Enable 'Developer Mode'\n")
    
    # Wait for user confirmation
    input("After you have enabled Developer Mode, press Enter to continue...\n")
    
    # Step 10: Open the extracted .msix folder for the user
    print("Opening the extracted .msix folder for you...")
    try:
        os.startfile(msix_extract_dir)  # Works on Windows
    except AttributeError:
        # Fallback (shouldn't be needed on Windows)
        subprocess.Popen(["explorer", msix_extract_dir])

    # Show remaining instructions
    print("\nI have opened a folder for you. Press Shift + right-click on a blank space in that folder, and select 'Open PowerShell Window Here'")
    print("Afterwards, paste this command in the opened PowerShell window:")
    print("Add-AppPackage -Register .\\AppxManifest.xml")
    print("And then you're done!")
    print("\nCredit to: u/z3r0nyaa on Reddit for the steps on how to install.")
    print("Like the script? Star it on Github!")

    input("\nPress Enter to exit...")
