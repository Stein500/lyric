import cv2
import numpy as np
import os
import glob
import subprocess
import imageio_ffmpeg

def apply_zoom_and_shake(img, zoom, shake_x=0, shake_y=0):
    h, w = img.shape[:2]
    crop_h = int(h / zoom)
    crop_w = int(w / zoom)
    
    start_y = (h - crop_h) // 2 + shake_y
    start_x = (w - crop_w) // 2 + shake_x
    
    start_y = max(0, min(start_y, h - crop_h))
    start_x = max(0, min(start_x, w - crop_w))
    
    cropped = img[start_y : start_y + crop_h, start_x : start_x + crop_w]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)

def generate_scene_frame(img, frame_idx, frames_per_scene, zooms):
    zoom = zooms[frame_idx]
    shake_x, shake_y = 0, 0
    beat_frame = frame_idx % 12.5
    if beat_frame < 3:
        intensity = int(12 * (1 - beat_frame / 3.0))
        shake_x = np.random.randint(-intensity, intensity + 1)
        shake_y = np.random.randint(-intensity, intensity + 1)
        
    return apply_zoom_and_shake(img, zoom, shake_x, shake_y)

def render_slideshow(image_paths, output_video_path, audio_path, is_vertical=True):
    width, height = (1080, 1920) if is_vertical else (1920, 1080)
    fps = 25
    scene_dur = 4.0
    trans_dur = 0.8
    
    frames_per_scene = int(scene_dur * fps)
    frames_trans = int(trans_dur * fps)
    
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Error loading image: {path}")
            return
        h, w = img.shape[:2]
        if (w, h) != (width, height):
            target_aspect = width / height
            aspect = w / h
            if aspect > target_aspect:
                new_w = int(h * target_aspect)
                start_x = (w - new_w) // 2
                cropped = img[:, start_x : start_x + new_w]
            else:
                new_h = int(w / target_aspect)
                start_y = (h - new_h) // 2
                cropped = img[start_y : start_y + new_h, :]
            img = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_AREA)
        images.append(img)

    num_scenes = len(images)
    total_frames = num_scenes * frames_per_scene - (num_scenes - 1) * frames_trans
    
    print(f"Rendering slideshow (streaming mode): {num_scenes} scenes, {total_frames} frames...")
    
    zooms = np.linspace(1.0, 1.08, frames_per_scene)
    
    temp_avi = "temp_render.avi"
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_writer = cv2.VideoWriter(temp_avi, fourcc, fps, (width, height))
    
    for i in range(num_scenes):
        non_trans_count = frames_per_scene - frames_trans
        for f in range(non_trans_count):
            frame = generate_scene_frame(images[i], f, frames_per_scene, zooms)
            video_writer.write(frame)
            
        if i < num_scenes - 1:
            for t in range(frames_trans):
                alpha = t / float(frames_trans)
                f_curr_idx = non_trans_count + t
                frame_curr = generate_scene_frame(images[i], f_curr_idx, frames_per_scene, zooms)
                frame_next = generate_scene_frame(images[i+1], t, frames_per_scene, zooms)
                blended = cv2.addWeighted(frame_curr, 1.0 - alpha, frame_next, alpha, 0)
                video_writer.write(blended)
        else:
            for f in range(non_trans_count, frames_per_scene):
                frame = generate_scene_frame(images[i], f, frames_per_scene, zooms)
                video_writer.write(frame)
                
    video_writer.release()
    
    ss_audio = 15.0
    duration_audio = total_frames / float(fps)
    
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_bin, "-y",
        "-i", temp_avi,
        "-ss", str(ss_audio), "-t", str(duration_audio), "-i", audio_path,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "ultrafast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        output_video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_avi):
        os.remove(temp_avi)
        
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("FFmpeg merge failed.")

def main():
    vertical_paths = [f"social_fancy_story/quote_{i:02d}_story.jpg" for i in range(1, 11)]
    render_slideshow(
        vertical_paths,
        "extrait_fancy_slideshow_vertical_9x16.mp4",
        "I_m_Not_Dying_Daïsky.mp3",
        is_vertical=True
    )
    
    square_paths = [f"social_fancy_square/quote_{i:02d}_square.jpg" for i in range(1, 11)]
    render_slideshow(
        square_paths,
        "extrait_fancy_slideshow_landscape_16x9.mp4",
        "I_m_Not_Dying_Daïsky.mp3",
        is_vertical=False
    )

if __name__ == "__main__":
    main()
