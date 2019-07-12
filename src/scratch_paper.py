ffmpeg_dir = context.ffmpeg_dir
extension_type = context.extension_type
vf_encode = context.vf_encode
frame_rate = context.frame_rate




create_video_from_scenes_command = "[ffmpeg_dir] -loglevel 0 -nostats -framerate [frame_rate] -start_number [start_number] -i [input_frames] -vframes [end_number] -vf deband [output_file]"
