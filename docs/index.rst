Dandere2x Overview
=======================================

.. meta::
   :description lang=en: Automate building, versioning, and hosting of your technical documentation continuously on Read the Docs.


Dandere2x reduces the time needed for Waifu2x to upscale animation (sometimes live-action) videos by applying compression techniques. Just as Netflix uses compression to quickly stream videos to your home, Dandere2x uses compression to expedite the waifu2x upscaling process.

Fast
    Dandere2x can provide a dramatic speedup for anime upscaling.
    In this comparison video_,  Dandere2x took only 3.5 minutes, while 
    using Video2x's lossless upscaling took 18 minutes!
    
.. _video: http://www.python.org/

Easy
   Dandere2x comes included with a GUI interface to make Dandere2x easy and fast to use, for both experienced and inexperienced users.
   
Customizable and Open Source
    Dandere2x is highly customizable and modifiable. In theory, Dandere2x can be applied to any CNN based upscaling algorithm -
    not just Waifu2x! Experienced users are also free to play with the .json file to find settings that best suits their needs. 
    
.. _Read the docs: http://readthedocs.org/

Help and Resources
==================

Reddit
   Reddit is the primary medium of communication for Dandere2x. If you want help, this is the best place to get an answer.  Usually, if I spend a night working on something, I'll do a short write up about it the night of.

Link: https://www.reddit.com/r/Dandere2x/


Telegram
   The telegram server for Dandere2x can be found here:
   The telegram can be seen as a means for immediate help or general discussion, although due to the school year starting I'm not sure how active I will be. 

Link: https://t.me/joinchat/KTRznBIPPNCbHkUqnwT8pA

Donations
   Dandere2x is 100% free and will always be 100% free. If you wish to contribute to dandere2x development, feel free to send me some  change! Funds go-to playing games with friends and food. 

Donation Links:
   Paypal_
   
   Patreon_

.. _Paypal: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=thatweeblife%40gmail.com&currency_code=USD&source=url 

.. _Patreon: https://www.patreon.com/dandere2x/

Downloading And Using Dandere2x
===============================

Dandere2x is still in development, but you can download and use the beta-candidate release here!

https://github.com/aka-katto/dandere2x/releases/tag/1.2.3bc2


Dandere2x JSON Settings
=======================
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
====================

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


Recommended Settings
====================

Although I personally don't have any preference, I go by ear and only upscale 1-2 seconds to see how the quality will turn out, before deciding to upscale a full video. However, a reddit users posted his findings, which I believe to be universal to many. 

https://www.reddit.com/r/Dandere2x/comments/cba28h/best_d2x_settings/

Naizuri77's rule of thumb:


.. code-block:: python

    block_size = 20
    quality_minimum = 80

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

