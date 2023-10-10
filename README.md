# Blender Non-Uniform scale fix

## Overview

When modeling for MSFS 2020 there is a restriction - only positive scale is allowed and only uniform 1 scale is advised. This addon (and script) transforms vertices positions and objects positions so they would stay the same (almost) and there will be no warnings on import.

---

## Addon Installation

- Open Blender
- Click Edit->Preferences
- Click Install
- Locate fix_scale_addon.py
- Double click it
- Enable Addon

---

## Usage

### Addon

In 3D view click Tool on the right side (press N if not visible). Addon adds two buttons and checkbox. They all located in Non-Uniform Scale Fix section.
1. (Button) Select Non-Uniform Scale - selects all objects in scene with non uniform 1 scale
2. (Button) Fix Non-Uniform Scale - Fixes scale in scene or for selected object
3. (Checkbox) Selected only - will fix only selected objects.

---

### Script

Optional script if you want to iterate fast thru the main logic - simply open fix_scale_script.py in Scripting view in Blender order to modify or run script. This script always fixes every object in scene.

## Important notes

- Addon is tested on Bldner v3.3.x LTS (current supported with msfs addon)
- This transformation WILL break mesh normals, so you'll need to fix them manually
- I developed this addon for myself, so if you want to expand/collaborate feel free to fork or open pull request

---