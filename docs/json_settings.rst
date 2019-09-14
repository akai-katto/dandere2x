JSON Settings
=============


Dandere2x JSON Settings
***********************

Basic Settings
--------------

The basic settings can be found under the 'usersettings' in the JSON and are choosable settings in the GUI. 

+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| JSON parameter |                                                      | description                                                                                                        |
|                | values                                               |                                                                                                                    |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
|                | Any positive integer                                 |                                                                                                                    |
| block_size     |                                                      | The block size of macro-blocks when computing block matches.                                                       |
|                |                                                      |                                                                                                                    |
|                |                                                      | The developer highly encourages block sizes between 15-30.                                                         |
|                |                                                      |                                                                                                                    |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| quality_min    | Integers [1-100]                                     | The minimum MSE quality loss dictated a block can have, when                                                       |
|                |                                                      | compared to how JPEG quantizes a block in a certain region.                                                        |
|                |                                                      |                                                                                                                    |
|                |                                                      |                                                                                                                    |
|                |                                                      | The developer discourges the use of this value being between 90-100,                                               |
|                |                                                      | as the visual blemishes produced by JPEG between these values are indistinguishable,                               |
|                |                                                      | and greatly increases Dandere2x's runtime.                                                                         |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| waifu2x_type   | 'vulkan', 'converter_cpp', 'caffe'                   | The implementation of waifu2x to use.                                                                              |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| denoise_level  | Integers [0-3]                                       | Waifu2x denoising level.                                                                                           |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| scale_factor   | Integers [0-4] (dependent on Waifu2x implementation) | How much to scale an image. As it currently stands, vulkan only offers 2x scaling for the model used in Dandere2x. |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| input_file     | String                                               | Input File                                                                                                         |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+
| output_file    | String                                               | Output file, when realtime_encoding is set to true.                                                                |
+----------------+------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------+


Advanced Settings
-----------------

The more advanced settings can be found under 'developer_settings' in the JSON. These are not modifiable in the GUI. 

                                                                                                                   |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| JSON Parameter                 |                          | description                                                                                                                                                    |
|                                | values                   |                                                                                                                                                                |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                | any positive integer     | The starting step size for Diamond Search when detecting similar blocks                                                                                        |
| step_size                      |                          |                                                                                                                                                                |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| bleed                          | any non-negative integer | How much bleeding to allow when constructing 'difference' images. The bigger the bleed, the amount of pixels waifu2x must process grows exponentially.         |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| debug                          | boolean                  | Output debug images, which is useful for detecting whether or not Dandere2x is behaving optimally                                                              |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| realtime_encoding              | boolean                  | Start encoding Dandere2x's frames into videos during runtime, and concontate all the videos at the end. This reduces overall runtime experienced by the user.  |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| realtime_encoding_delete_files | boolean                  | Leave off - When it works, this option deletes workspace files during runtime, reducing the amount of used storage.                                            |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| workspace_use_temp             | boolean                  | Operate out of the %temp% folder for the user.                                                                                                                 |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| workspace                      | directory                | If workspace_use_temp is false, operate out of this directory instead.                                                                                         |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| dandere2x_cpp_dir              | directory                | Location of the Dandere2x_Cpp binary.                                                                                                                          |
+--------------------------------+--------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+


FFMPEG JSON Settings
********************

Frames to Video
---------------

Dandere2x is heavily reliant FFMPEG video filters in order to work correctly. 

.. code-block:: python

    "frames_to_video": {
      "output_options": {
      .....
        "-vf": ["deband=range=22:blur=false","pp7=qp=4:mode=medium"]
       .....
      },
    },

Without debanding and pp7, Dandere2x would have compression artifacts. Dandere2x is very dependent on these filters helping deblock and denoise the artifacts produced by Dandere2x. 

Image Examples Provided by Reddit User Naizuri77

https://imgur.com/a/2AOXsC7

Video to Frames
---------------

This is a really weird one - Dandere2x_CPP behaves better when we add noise (this same noise is always removed by Waifu2x when noise level > 2). Props to reddit user Judas0001 in his post here finding this optimization trick. You can read his full explanation here

https://www.reddit.com/r/Dandere2x/comments/bp5n8o/dandere2x_0712_impressions_and_other_stuff/

.. code-block:: python

    "video_to_frames": {
      "output_options": {
      ....
        "-vf": ["noise=c1s=8:c0f=u"]
      ....
      }
    },

It seems when a compression codec processes macroblocks, Dandere2x is unable to identify those changes as movement, and as a result, flags the block as needed to be re-drawn. Adding noise at a consistent rate helps balance out these macro-block changes, although this is just pure speculation. Without this, Dandere2x preforms much worse. 
