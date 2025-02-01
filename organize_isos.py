import os
import shutil
from datetime import datetime
from flask import Flask, render_template_string, redirect, url_for

# Environment variable for ISO directory
ISO_DIR = os.getenv("ISO_DIR", "/mnt/user/isos")

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
    return render_template_string(HTML_TEMPLATE, isos=get_iso_files())

# Route to trigger ISO organization
@app.route('/organize')
def organize():
    organize_isos()
    return redirect(url_for('index'))

# Function to organize ISOs based on modification date and naming conventions
def organize_isos():
    for root, dirs, files in os.walk(ISO_DIR):
        for file in files:
            if file.endswith(".iso"):
                src_path = os.path.join(root, file)
                mod_time = datetime.fromtimestamp(os.path.getmtime(src_path)).strftime("%Y-%m-%d")
                new_name = f"{mod_time}_{file.lower().replace(' ', '_')}"
                dest_path = os.path.join(ISO_DIR, new_name)

                if src_path != dest_path:
                    if not os.path.exists(dest_path):
                        shutil.move(src_path, dest_path)
                        print(f"Renamed: {src_path} -> {dest_path}")
                    else:
                        print(f"Duplicate found: {src_path} (already exists as {dest_path})")

# Run the Flask app on port 1337
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
