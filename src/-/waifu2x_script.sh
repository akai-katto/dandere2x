cd /home/linux/Documents/waifu2x/
th /home/linux/Documents/waifu2x/dandere.lua -m noise_scale -noise_level 3 -i -inputs\frame1.jpg -o -merged\merged_1.jpg

th /home/linux/Documents/waifu2x/dandere.lua -m noise_scale -noise_level 3 -resume 1 -l -frames.txt -o -upscaled\output_%d.png
