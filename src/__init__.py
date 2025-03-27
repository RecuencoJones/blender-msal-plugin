from pathlib import Path
import tomllib
from pkg_resources import packaging


manifest_file = Path(__file__).parent / "blender_manifest.toml"

with open(manifest_file, "rb") as f:
    manifest = tomllib.load(f)

bl_info = {
    "name": manifest["name"],
    "version": packaging.version.parse(manifest["version"]).release,
    "blender": packaging.version.parse(manifest["blender_version_min"]).release,
    "author": "David Recuenco",
    "location": "Operator search",
    "description": manifest["tagline"],
    "category": "System",
}

bl_info_version = bl_info["version"]
bl_info_name = bl_info["name"]


def register():
    from . import plugin

    plugin.register()


def unregister():
    from . import plugin

    plugin.unregister()
