Dandere2x Overview
==================

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

