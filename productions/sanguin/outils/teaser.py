#!/usr/bin/env python3
"""Create a 15-second portrait teaser from the enhanced full version and its artist audio."""
from pathlib import Path
import imageio_ffmpeg, subprocess
root=Path(__file__).resolve().parent.parent
src=root/'livrables/SANGUIN-DSKY-COMPLET-ENRICHI.mp4'
out=root/'livrables/SANGUIN-DSKY-TEASER-15s.mp4'
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-ss','24.166667','-i',str(src),'-filter_complex','[0:v]setsar=1,format=yuv420p[v]','-map','[v]','-map','0:a:0','-t','15','-r','30','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:v','libx264','-preset','veryfast','-crf','22','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(out)],check=True)
print(out)
