import subprocess, json, re
FF="work/bin/ffmpeg"; SRC="Guerrier* Daïsky.mp3"; OUT="work/master_guerrier.mp3"
DUR=206.40
err = subprocess.run([FF,"-hide_banner","-i",SRC,"-af","loudnorm=print_format=json","-f","null","-"],capture_output=True,text=True).stderr
m = json.loads(re.search(r"\{.*\}", err, re.S).group(0))
print("mesure:", {k:m[k] for k in ("input_i","input_tp","input_lra","input_thresh","target_offset")})
# TP cible -2.2 en linear pour atterrir <= -1.5 dBTP apres overshoot MP3 (mesure empirique)
chain = (f"highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-2.2:LRA=11:"
 f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
 f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run([FF,"-y","-v","error","-i",SRC,"-af",chain,"-t",str(DUR),
 "-c:a","libmp3lame","-b:a","320k","-ar","48000",OUT],check=True)
v = subprocess.run([FF,"-hide_banner","-i",OUT,"-af","loudnorm=print_format=json","-f","null","-"],capture_output=True,text=True).stderr
j = json.loads(re.search(r"\{.*\}", v, re.S).group(0))
print("master final:", j["input_i"], "LUFS /", j["input_tp"], "dBTP")
