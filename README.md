# Alfawise_U20Mix_for_Cura


This repository, publicly available, is my configuration for using an Alfawise U20 Mix (Weedo ME40 Pro clone) with mainstream Cura (4.8 for now). Because WiiBuilder2, custom software delivered with printer, is not good enough for advanced use.


.


## There is some files to add to your Cura install directory :


### definitions/alfawise_u20mix.def.json
  This is printer description, with good start & stop g-code (alfawise software based).
  Thanks to Samuel Pinches for the Cura Alfawise U20 def file, that give me some ideas on "how to do".

### definitions/alfawise_u20mix_solo.def.json
  Same printer definition but with ONLY left extruder used.
  Start & stop g-code stay compatible with filament extrusion norms, so can mix easily mono or bifilament prints.

.


### extruders/alfawise_u20mix_extruder_1.def.json
### extruders/alfawise_u20mix_extruder_2.def.json
  These are extuders descriptions, based on some Ultimaker ones.
  

.


### plugins/PostProcessingPlugin/scripts/CreateThumbnailU20Mix.py
  A script to create a thumbnail (JPEG 180x180 picture) embedded into generated G-CODE.
  Based on Cura's CreateThumbnail.py


.


Hope it will helps until real manufacturer support for Cura.
