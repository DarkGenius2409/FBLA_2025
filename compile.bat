ffmpeg -f image2 -r 60 -i ./output/frames/screen_%%09d.png -vcodec mpeg4 -y ./output/%1.mp4
del /q output\frames\*
for /d %%x in (output\frames\*) do @rd /s /q "%%x"