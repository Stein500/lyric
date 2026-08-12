import cv2
import os

def resize_and_crop(img, target_width, target_height):
    h, w = img.shape[:2]
    target_aspect = target_width / target_height
    aspect = w / h
    
    if aspect > target_aspect:
        # Image is too wide: crop horizontally
        new_w = int(h * target_aspect)
        start_x = (w - new_w) // 2
        cropped = img[:, start_x : start_x + new_w]
    else:
        # Image is too tall: crop vertically
        new_h = int(w / target_aspect)
        start_y = (h - new_h) // 2
        cropped = img[start_y : start_y + new_h, :]
        
    # Resize to final target size
    return cv2.resize(cropped, (target_width, target_height), interpolation=cv2.INTER_AREA)

def main():
    # Look for the new cover art or fallback
    candidates = [
        "post_single_square_1080.jpg",
        "artwork_lyric_quote.jpg",
        "cover.jpg"
    ]
    
    src_path = None
    for cand in candidates:
        if os.path.exists(cand):
            src_path = cand
            break
            
    if src_path is None:
        print("Error: No source image found to generate social images.")
        return
        
    print(f"Reading source image: {src_path}")
    img = cv2.imread(src_path)
    if img is None:
        print("Error: Could not read image.")
        return
        
    os.makedirs("social_images", exist_ok=True)
    
    # 10 Social Media image sizes (Width, Height, Label)
    sizes = [
        (1080, 1080, "1_instagram_square_feed_1080x1080.jpg"),
        (1080, 1920, "2_story_status_tiktok_9x16_1080x1920.jpg"),
        (1920, 1080, "3_youtube_thumbnail_landscape_16x9_1920x1080.jpg"),
        (2560, 1440, "4_youtube_banner_2560x1440.jpg"),
        (1500, 500,  "5_twitter_header_3x1_1500x500.jpg"),
        (1584, 396,  "6_linkedin_banner_4x1_1584x396.jpg"),
        (820, 312,   "7_facebook_cover_820x312.jpg"),
        (1000, 1500, "8_pinterest_pin_2x3_1000x1500.jpg"),
        (1080, 1350, "9_instagram_portrait_4x5_1080x1350.jpg"),
        (500, 500,   "10_linktree_profile_avatar_500x500.jpg")
    ]
    
    for w, h, name in sizes:
        out_path = os.path.join("social_images", name)
        resized = resize_and_crop(img, w, h)
        cv2.imwrite(out_path, resized, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        print(f"Generated: {out_path} ({w}x{h})")
        
    print("\nSuccessfully generated all 10 social images!")

if __name__ == "__main__":
    main()
