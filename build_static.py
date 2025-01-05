import os
import shutil
from pathlib import Path

def build_static():
    # Create static directory
    static_dir = Path("static")
    if static_dir.exists():
        shutil.rmtree(static_dir)
    static_dir.mkdir()

    # Copy all HTML files directly to static directory
    templates_dir = Path("app/templates/admin")
    if templates_dir.exists():
        for template in templates_dir.rglob("*.html"):
            dest_path = static_dir / template.name
            shutil.copy2(template, dest_path)
    
    # Copy index.html if it exists in templates
    index_template = Path("app/templates/index.html")
    if index_template.exists():
        shutil.copy2(index_template, static_dir / "index.html")

    # Copy static assets (CSS, JS, images)
    static_assets = Path("app/static")
    if static_assets.exists():
        for asset in static_assets.rglob("*.*"):
            relative_path = asset.relative_to(static_assets)
            dest_path = static_dir / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, dest_path)

    # Create a simple index.html if it doesn't exist
    index_path = static_dir / "index.html"
    if not index_path.exists():
        with open(index_path, "w") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>ERP System</title>
    <meta http-equiv="refresh" content="0;url=dashboard.html">
</head>
<body>
    <p>Redirecting to dashboard...</p>
</body>
</html>
            """)

if __name__ == "__main__":
    build_static()