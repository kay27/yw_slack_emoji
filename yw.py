from PIL import Image, ImageDraw, ImageFont, ImageOps
import math

size = (128, 128)  # GIF dimensions
num_frames = 16  # Number of frames in the GIF
duration = 1000 / num_frames  # Duration per frame in milliseconds
sector_colors = ["#5010F0", "#8A2BE2"]  # Blue and Violet

# Create frames
frames = []
angle_shift_per_frame = 60 / num_frames  # Total rotation across frames

font_size = 72  # Base font size for "YW"
font = ImageFont.truetype("arial.ttf", font_size)  # Using a standard larger font

for frame_idx in range(num_frames):
    img = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(img)

    # Fill the image with colored sectors
    cx, cy = size[0] // 2, size[1] // 2  # Center of the image
    for x in range(size[0]):
        for y in range(size[1]):
            angle = (math.degrees(math.atan2(y - cy, x - cx)) + 360) % 360
            shifted_angle = (angle + frame_idx * angle_shift_per_frame) % 360
            sector_idx = int(shifted_angle // 30)
            draw.point((x, y), fill=sector_colors[sector_idx % 2])

    # Animate "YW" text
    text = "YW"
    
    # Pulsation effect
    scale_factor = 1 + 0.1 * math.sin(2 * math.pi * frame_idx / num_frames)
    current_font = ImageFont.truetype("arial.ttf", int(font_size * scale_factor))
    
    # Measure text size
    text_size = draw.textsize(text, font=current_font)
    
    # Swinging effect
    rotation_angle = 12 * math.sin(2 * math.pi * frame_idx / num_frames)
    
    # Create text image with alpha channel
    text_img = Image.new("RGBA", text_size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    
    # Draw black outline
    text_draw.text((0, 0), text, font=current_font, fill="black", stroke_width=3, stroke_fill="black")
    
    # Draw white fill
    text_draw.text((0, 0), text, font=current_font, fill="white")
    
    # Rotate the text image
    rotated_text = text_img.rotate(rotation_angle, expand=True)
    
    # Paste centered
    text_position = ((size[0] - rotated_text.size[0]) // 2, (size[1] - rotated_text.size[1]) // 2)
    img = img.convert("RGBA")
    img.paste(rotated_text, text_position, rotated_text)
    
    frames.append(img.convert("RGB"))

# Save GIF
output_path = "yw.gif"
frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=duration, loop=0)

output_path
