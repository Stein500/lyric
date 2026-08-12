import json
import os

def create_ass_subtitles(json_path, ass_path, is_vertical=False):
    if not os.path.exists(json_path):
        print(f"Warning: {json_path} does not exist yet. Skipping ASS generation.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        lyrics = json.load(f)
        
    # Filter out section headers
    lines = [item for item in lyrics if not item.get('isSection')]
    
    # Configure font sizes and alignments
    if is_vertical:
        font_size = 48
        margin_v = 400 # High margin to avoid TikTok UI overlays
        alignment = 2  # Centered bottom
        style_def = f"Style: Default,DejaVu Sans,{font_size},&H00FFFFFF,&H000000FF,&H00050212,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,{alignment},30,30,{margin_v},1"
        style_highlight = f"Style: Highlight,DejaVu Sans,{font_size + 4},&H0000D0FF,&H000000FF,&H00050212,&H00000000,-1,0,0,0,100,100,0,0,1,3.5,0,{alignment},30,30,{margin_v},1"
    else:
        font_size = 32
        margin_v = 120 # From bottom
        alignment = 2  # Centered bottom
        style_def = f"Style: Default,DejaVu Sans,{font_size},&H00FFFFFF,&H000000FF,&H00050212,&H00000000,-1,0,0,0,100,100,0,0,1,2.5,1.5,{alignment},50,50,{margin_v},1"
        style_highlight = f"Style: Highlight,DejaVu Sans,{font_size + 2},&H0000D0FF,&H000000FF,&H00050212,&H00000000,-1,0,0,0,100,100,0,0,1,3.0,1.5,{alignment},50,50,{margin_v},1"

    header = f"""[Script Info]
Title: I'm Not Dying
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: {1080 if is_vertical else 1920}
PlayResY: {1920 if is_vertical else 1080}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{style_def}
{style_highlight}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int((seconds % 1) * 100)
        return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

    events = []
    for i, line in enumerate(lines):
        start_time = line['time']
        
        # Determine end time
        if i < len(lines) - 1:
            next_start = lines[i+1]['time']
            if next_start - start_time > 4.5:
                end_time = start_time + 3.8
            else:
                end_time = next_start
        else:
            end_time = start_time + 4.0
            
        start_str = format_time(start_time)
        end_str = format_time(end_time)
        text = line['text']
        
        text = text.replace('"', '\\"')
        styled_text = f"{{\\\\fad(150,150)}}{text}"
        
        style = "Highlight" if "Wolof TechStein" in text else "Default"
        events.append(f"Dialogue: 0,{start_str},{end_str},{style},,0,0,0,,{styled_text}")
        
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write("\n".join(events))
        f.write("\n")
        
    print(f"Generated ASS subtitle file: {ass_path}")

if __name__ == "__main__":
    create_ass_subtitles("synced_lyrics.json", "lyrics_landscape.ass", is_vertical=False)
    create_ass_subtitles("synced_lyrics.json", "lyrics_vertical.ass", is_vertical=True)
