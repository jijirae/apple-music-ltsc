![Banner](https://i.ibb.co/1f7sGZdG/banner.png)
# 🍎 Apple Music on Windows 10 LTSC  
An Apple Music installer script for **Windows 10 LTSC (10.0.19044.0)**

Skips most of the boring steps like renaming and patching.

[![Python](https://img.shields.io/badge/python-3.x-blue.svg?logo=python)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Windows-10%20LTSC-0078D6?logo=windows)](https://www.microsoft.com/windows)

---

## ⚠️ Requirements
- **Windows 10 LTSC (10.0.19044.0)**  
- **Python 3.10.11** → [Download here](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)

---

## 📥 Downloading Apple Music  

1. Go to [https://store.rg-adguard.net/](https://store.rg-adguard.net/)  
2. Select **ProductId** on the left, and **Fast** on the right  
3. Enter this Product ID:  
`9PFHDD62MXS1`
4. Click on the **first result with `.msixbundle`** in its name  
- If it doesn’t download when clicked, right-click → **Copy Link**, then paste the link in a new browser tab  

---

## ⚙️ Installation Steps  

1. Create a folder and place both the downloaded **`.Msixbundle`** file and the `install.py` script inside.  
> ⚠️ You will not be able to move this folder later, so choose the location carefully.  

2. Run `install.py`  

3. After running the script, go to:  
`Settings → Windows Update → For Developers → Enable "Developer Mode"`

4. The script will open a folder for you. In that folder:  
- Press **Shift + Right-Click** on a blank space  
- Select **"Open PowerShell Window Here"**  

5. In the opened PowerShell window, paste and run this command:  
```powershell
Add-AppPackage -Register .\AppxManifest.xml
```
✅ That’s it! Apple Music should now be installed and working on LTSC.
🙌 Credits

Big thanks to u/z3r0nyaa on Reddit for the original steps.
[Source link](https://www.reddit.com/r/AppleMusic/comments/1fjmelg/comment/lpffkja/)
