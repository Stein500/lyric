import subprocess
import os

def render_video(output_path, is_vertical=False, ss=None, to=None):
    # Determine local square image
    square_img = "post_single_square_1080.jpg"
    if not os.path.exists(square_img):
        square_img = "cover.jpg"

    # Determine local vertical image
    story_img = "post_story_1080x1920.jpg"
    if not os.path.exists(story_img):
        story_img = None

    audio_file = "I_m_Not_Dying_Daïsky.mp3"

    # Construct the filter complex based on layout and inputs
    if is_vertical:
        if story_img:
            # OPTIMIZED: Scale to small resolution, blur, then upscale to 1080x1920 (saves 16x cpu!)
            filter_complex = (
                f"[0:v]scale=w='iw*max(270/iw\\,480/ih)':h='ih*max(270/iw\\,480/ih)',crop=270:480,boxblur=5:5,scale=1080:1920[bg]; "
                f"[1:v]scale=700:700[fg]; "
                f"[bg][fg]overlay=(main_w-700)/2:(main_h-700)/2-150[vid]; "
                f"[vid]subtitles=lyrics_vertical.ass[outv]"
            )
            inputs = ["-loop", "1", "-i", story_img, "-loop", "1", "-i", square_img]
        else:
            # Fallback to square image scaled, cropped, and blurred for background
            filter_complex = (
                f"[0:v]scale=w='iw*max(270/iw\\,480/ih)':h='ih*max(270/iw\\,480/ih)',crop=270:480,boxblur=5:5,scale=1080:1920[bg]; "
                f"[0:v]scale=700:700[fg]; "
                f"[bg][fg]overlay=(main_w-700)/2:(main_h-700)/2-150[vid]; "
                f"[vid]subtitles=lyrics_vertical.ass[outv]"
            )
            inputs = ["-loop", "1", "-i", square_img]
    else:
        # Landscape layout: OPTIMIZED: scale to small, blur, and upscale to 1920x1080
        filter_complex = (
            f"[0:v]scale=w='iw*max(480/iw\\,270/ih)':h='ih*max(480/iw\\,270/ih)',crop=480:270,boxblur=5:5,scale=1920:1080[bg]; "
            f"[0:v]scale=500:500[fg]; "
            f"[bg][fg]overlay=(main_w-500)/2:(main_h-500)/2[vid]; "
            f"[vid]subtitles=lyrics_landscape.ass[outv]"
        )
        inputs = ["-loop", "1", "-i", square_img]

    cmd = ["ffmpeg", "-y", "-threads", "0"]
    cmd.extend(inputs)
    cmd.extend(["-i", audio_file])
    
    # Add seeking options if specified
    if ss is not None and to is not None:
        cmd.extend(["-ss", str(ss), "-to", str(to)])
    
    # Add complex filter, mapping, encoding, and shortest flags
    # We map the audio from our MP3 input, which is input index 2 if story_img and vertical else 1
    audio_index = 2 if (is_vertical and story_img) else 1
    
    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", f"{audio_index}:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "ultrafast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k"
    ])
    
    # If rendering full video, use shortest since loop is 1
    if ss is None:
        cmd.append("-shortest")
        
    cmd.append(output_path)
    
    print(f"\n---> Running FFmpeg to generate: {output_path}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error rendering {output_path}:")
        print(result.stderr)
        raise RuntimeError(f"FFmpeg failed with exit code {result.returncode}")
    else:
        print(f"Successfully generated: {output_path}!")

def main():
    # Make sure ASS files are up-to-date
    import generate_ass
    generate_ass.create_ass_subtitles("synced_lyrics.json", "lyrics_landscape.ass", is_vertical=False)
    generate_ass.create_ass_subtitles("synced_lyrics.json", "lyrics_vertical.ass", is_vertical=True)

    # 1. Full Landscape Video (YouTube format)
    render_video("im_not_dying_landscape_16x9.mp4", is_vertical=False)
    
    # 2. Full Vertical Video (TikTok/Reels/Shorts format)
    render_video("im_not_dying_vertical_9x16.mp4", is_vertical=True)
    
    # 3. Extrait 1: Refrain (Chorus 1) (Vertical highlight, 21 seconds: 15s to 36s)
    render_video("extrait_refrain_9x16.mp4", is_vertical=True, ss=15.0, to=36.0)
    
    # 4. Extrait 2: Pont + Refrain 3 (Vertical highlight, 37 seconds: 137s to 174s)
    render_video("extrait_pont_refrain_9x16.mp4", is_vertical=True, ss=137.0, to=174.0)

if __name__ == "__main__":
    main()
