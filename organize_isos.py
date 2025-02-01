import os
import shutil
from datetime import datetime
from flask import Flask, render_template_string, redirect, url_for
app = Flask(__name__)

# Environment variables
ISO_DIR = os.getenv("ISO_DIR", "/mnt/user/isos")
OS_FOLDERS = {
    "Linux": ["linux", "ubuntu", "debian", "fedora", "centos", "arch", "kali"],
    "MacOS": ["macos", "osx", "mac", "darwin"],
    "Windows": ["windows", "win10", "win11", "win7", "win8"],
    "Windows_Server": ["server", "windows_server"],
    "pFSense": ["pfsense"],
    "VBIOS": ["vbios", "gpu_bios"],
    "Tools": ["tools", "drivers", "utilities", "install_tool"],
    "Virtio": ["virtio", "vm_drivers"]
}

# Initialize Flask app
app = Flask(__name__)

# HTML template for the web portal
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ISO Organizer</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        tr:hover { background-color: #f1f1f1; }
        a { text-decoration: none; color: #007BFF; }
        a:hover { text-decoration: underline; }
        button { padding: 8px 12px; background-color: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <h1>ISO Organizer</h1>
    <button onclick="window.location.href='{{ url_for('organize') }}'">Organize ISOs</button>
    <table>
        <tr><th>File Name</th><th>Last Modified</th></tr>
        {% for iso in isos %}
        <tr>
            <td>{{ iso['name'] }}</td>
            <td>{{ iso['mod_time'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Function to get ISO files and their modification times
def get_iso_files():
    isos = []
    for root, _, files in os.walk(ISO_DIR):
        for file in files:
            if file.endswith(".iso"):
                file_path = os.path.join(root, file)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                isos.append({"name": file, "mod_time": mod_time})
    return sorted(isos, key=lambda x: x["mod_time"], reverse=True)

# Home route to display the ISO files
@app.route('/')
def index():
    from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', isos=get_iso_files())

# Route to trigger ISO organization
@app.route('/organize')
def organize():
    organize_isos()
    return redirect(url_for('index'))

# Function to organize ISOs based on folder mappings
def organize_isos():
    for root, dirs, files in os.walk(ISO_DIR):
        for file in files:
            if file.endswith(".iso"):
                src_path = os.path.join(root, file)
                mod_time = datetime.fromtimestamp(os.path.getmtime(src_path)).strftime("%Y-%m-%d")
                new_name = f"{mod_time}_{file.lower().replace(' ', '_')}"
                dest_folder = determine_folder(file)
                dest_path = os.path.join(ISO_DIR, dest_folder, new_name)

                # Create destination folder if it doesn't exist
                if not os.path.exists(os.path.join(ISO_DIR, dest_folder)):
                    os.makedirs(os.path.join(ISO_DIR, dest_folder))

                # Move the file
                if src_path != dest_path:
                    if not os.path.exists(dest_path):
                        shutil.move(src_path, dest_path)
                        print(f"Moved: {src_path} -> {dest_path}")
                    else:
                        print(f"Duplicate found: {src_path} (already exists as {dest_path})")

# Determine folder based on file name
def determine_folder(filename):
    filename_lower = filename.lower()
    for folder, keywords in OS_FOLDERS.items():
        if any(keyword in filename_lower for keyword in keywords):
            return folder
    return os.getenv("UNRECOGNIZED_FOLDER", "Unrecognized")  # Move unrecognized ISOs here

# Run the Flask app on port 1337
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
