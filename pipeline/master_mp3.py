import subprocess, json, re, imageio_ffmpeg
ff = imageio_ffmpeg.get_ffmpeg_exe()
SRC = "Yafoy t'es encore là.mp3"
OUT = "livrables/Yafoy t'es encore là - Daïsky (Master).mp3"
# Pass 1
r = subprocess.run([ff,'-i',SRC,'-af','loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
m = json.loads(re.search(r'\{[^}]+\}', r.stderr).group(0))
print('pass1:', m)
af = (f"highpass=f=30,lowpass=f=18000,"
      f"loudnorm=I=-14:TP=-2.4:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
r2 = subprocess.run([ff,'-y','-i',SRC,'-af',af,'-t','244.99','-vn','-c:a','libmp3lame','-b:a','320k','-ar','48000',OUT],capture_output=True,text=True)
print('pass2 rc:', r2.returncode)
# verify
r3 = subprocess.run([ff,'-i',OUT,'-af','loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
v = json.loads(re.search(r'\{[^}]+\}', r3.stderr).group(0))
print('verify LUFS:', v['input_i'], 'TP:', v['input_tp'])
