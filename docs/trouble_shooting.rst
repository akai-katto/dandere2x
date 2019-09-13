Trouble Shooting Dandere2x
==========================


Before you start, check to make sure

A) Your drivers are up to date.

B) You are running Dandere2x.exe as administrator

C) The video file is FFMPEG compatible.

Problem: Dandere2x is Producing Black Frames / Video
----------------------------------------------------

This is a common issue with the waifu2x-ncnn-vulkan. Change the 'tile_size' in the waifu2x_ncnn_vulkan section of the dandere2x.json file to something smaller. The default for Dandere2x is 200, so try 100. 


Problem: I want Dandere2x to not operate out of %temp%. How do I do this?
-------------------------------------------------------------------------

In dandere2x.json, find the 'workspace_use_temp' flag and set it to false. Then, you can choose where to put the workspace using the 'workspace flag. 

