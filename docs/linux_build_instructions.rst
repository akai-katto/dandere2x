Building Dandere2x On Linux
===========================



We from Dandere2x primarily recommend using an Arch-based distribution or as a second option any other distro with Snap installed and working - Ubuntu to be short. We will give you the instructions on how to install the dependencies and running Dandere2x in a moment.

Installing dependencies
***********************

Waifu2x with Snap
-----------------

This is the easier part, just open up a terminal and run the following command:

    ``sudo snap install waifu2x-ncnn-vulkan --edge``

The problem is that this is a pretty old version of waifu2x hence why we recommend an Arch-based distro.

And just make sure you got the graphics driver installed based on your distro, Vulkan and OpenCL stuff for guarantee.


Waifu2x on an Arch-based distro
------------------------------

If you haven't got a working AUR helper (we recommend yay), just open a terminal and

    ``sudo pacman -S git && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si``

And if you haven't enabled the multilib repository on pacman.conf, edit this file

    ``sudo nano /etc/pacman.conf``

And uncomment the lines:

    ``[multilib]``

    ``Include = /etc/pacman.d/mirrorlist``

Now you have access to the AUR.

We strongly recommend using the waifu2x-ncnn-vulkan client because it's the fastest one we tested.

The waifu2x-converter-CPP client is more "compatible" overhaul but its about 40% slower than the Vulkan one.

If you want to use the Vulkan client

    ``yay -Syu ncnn-git waifu2x-ncnn-vulkan-git``

If you want to use the converter-cpp version

    ``yay -Syu waifu2x-converter-cpp``

For both ones, you should have the appropriate GPGPU and OpenCL loaders just to be sure everything will work and the Vulkan stuff. 

For the OpenCL part, there's an awesome page on the `Arch Wiki <https://wiki.archlinux.org/index.php/GPGPU>`_ on how to do it.

For the Vulkan counterpart, there's also a `page <https://wiki.archlinux.org/index.php/Vulkan>`_ on it.

Python modules
--------------

First, install pip and python3 if you haven't got it already.

For an Arch-based distro,

    ``sudo pacman -Syu python-pip python``

And for a Ubuntu-based distro,

    ``sudo apt update && sudo apt install python3-pip python3``

That should do it for the Python package manager, now open a terminal inside the ``dandere2x/src/`` dir and run a 

    ``pip install -r requirements.txt --user``


Compiling the CPP binary
************************


Using our simple script
-----------------------

We include a simple bash script to do this for you there are a few dependencies: make, cmake and a compiler.

We recommend you install the "base development" package on your distro like so:

For an Arch-based distro

    ``sudo pacman -Syu base-devel``

For a Ubuntu-based distro

    ``sudo apt-get install build-essential``

And you should have everything to get the CPP part right.

Open a terminal in the root folder of the cloned dandere2x project from GitHub and

    ``sh cppstuff.sh``

Important: you **have** to be on the root folder of the project, you can verify it by running ``pwd`` and verifying it ends with "/dandere2x"

Note: this moves the binary to the **default** path for it to be.


Manually compiling and moving the binary
----------------------------------------

If you for some reason can't or don't want to run the script, you can do this manually by compiling and moving the binary to the default or your desired and configured path

To compile it:

    ``cd ../dandere2x_cpp``

    ``cmake CMakeLists.txt``

    ``make``

Then move the file ``dandere2x_cpp/dandere2x_cpp`` to ``src/externals/dandere2x_cpp``


Usage
=====

There are two main ways you can use Dandere2x: the GUI way and the terminal way.

Keep in mind that you do have more control over what's happening with the terminal way than the GUI way, but you lose practicality.


GUI way
-------

Inside the ``dandere2x/src`` directory, run

    ``python gui_driver.py``

We recommend you use the **Vulkan** client of Waifu2x when using Dandere2x.

Select the file you want to upscale, the output file, denoise level, image quality, and block size and simply hit that big button Upscale!


Terminal way
------------

First, edit the ``dandere2x_linux.json`` file to configure everything.

The most important parts are the sections ``dandere2x/usersettings`` and your selected waifu2x client.

You have to configure a valid binary file in the ``yourWaifu2xClient/yourWaifu2xClient_path`` and ``yourWaifu2xClient/yourWaifu2xClient_file_name``. The ``path`` is the root directory of it and the ``file_name`` is the binary on what client you'll use.

For example, if the binary is in the following place: ``/usr/bin/waifu2x-converter-cpp``, the ``_path`` option must be ``/usr/bin/`` and the ``file_name`` be ``waifu2x-converter-cpp`` only.

You can leave these two options blank or linked with a non-existing file and Dandere2x will try finding a (currently only Vulkan) client of Waifu2x on the system and asking you which one you want to use. This can be the Snap or waifu2x-ncnn-vulkan binaries here. 

Important note: The two versions of waifu2x Vulkan (Snap and AUR) are **not** interchangeable internally. Dandere2x choses what version to run internally based on if the word "snap" is present in the ``file_path`` option in the ``dandere2x_linux.json`` file.
 
The next part you have to look closely is the ``dandere2x/usersettings``. Here is where you give Dandere2x the file to work on, block size, working image quality (not final video quality), denoise level, and ``waifu2x_type``.

``waifu2x_type`` for Linux you basically will only use either ``vulkan`` or ``converter_cpp``.

Then give Dandere2x a ``input_file`` and ``output_file``, inside ``dandere2x/src`` dir run:

    ``python scratch_paper.py``

And voilà, you're done.

Note: ".." in the JSON configuration file means the root folder of where you are calling Dandere2x from. For example, if you're on the ``dandere2x/src`` dir (that you should be otherwise it'll probably not work), "../workspace" is the directory ``dandere2x/src/workspace``.

Windows Operating System
************************

aka_katto, pls help


For Developers
##############


Advanced stuff explained here...

Contributing section as well?




Links
#####

`Subreddit <https://www.reddit.com/r/Dandere2x/>`_

`Telegram Server <https://t.me/joinchat/KTRznBIPPNCbHkUqnwT8pA>`_

`Patreon <https://www.patreon.com/dandere2x>`_



License
#######

Dandere2x is licensed under the GPL v3.
