# Tile markers

## Installation
Download this repository as a zip ('<> code' button) then install the zip as an addon through Blender (Edit > Preferences > Add-ons > Install)

## Activation
Activate the addon by pressing the keybind (default: ctrl + shift + F9) or the button (Object > Tile markers).

Activating it will:
- Create a grease pencil if one created by this addon does not exist.
- Put you in paint mode of the pencil if you were not already in it.
- Put you in object mode if you were in paint mode of the pencil.

(This acts like a toggle.)

## Usage
The pencil will have two types of materials: draw and erase.

Drawing will check each object that was drawn over and then delete the strokes.

For each location under the stroke the following must be met:
- To create a tile marker
    - The 'map' object must be specified in the config panel.
    - The front object at the location must be the 'map'; another object could be in front, blocking it from the pencil's view.
    - The material used must be a 'draw' material and must have an associated 'marker' material to use for the tile marker (configurable).
    - Another tile cannot have been created at the location during the current stroke (to prevent duplicates).
    - The location must be a multiple of the tile size (configurable), acting like a grid starting from (0, 0, 0).

- To delete a tile marker
    - The front object at the location must be a tile marker (created by the addon); another object could be in front, blocking it from the pencil's view.
    - The material used must be the 'erase' material.

## Config panel
The config panel can be accessed from the 'N panel' > Create > Tile markers.

Here you can customise the following:
- The size of each tile marker (square). This does not affect existing markers.
- The map object. This is the object that tile markers are created from, mimicking its surface.
- The erase material.
- The marker types. Each marker type has three components: name, draw material and marker material. The name is cosmetic for this panel only.
The draw material is added to the gpencil and when a tile marker is created with it, the corresponding marker material will be used.

Not all settings will update automatically; you may need to toggle out of draw mode (or even delete the pencil) then toggle back in (using the addon).