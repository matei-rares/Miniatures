from PIL import Image, ImageFilter
import os
import math

def make_collage_full_rows(folder, output_file="collage.png", columns=5, blur_strength=0, bg_color="white"):
    # Collect PNG images
    image_files = [os.path.join(folder, f) for f in os.listdir(folder)
                   if f.lower().endswith(".png")]

    if not image_files:
        print("No PNG images found in folder:", folder)
        return

    # Use first image resolution as reference
    first_img = Image.open(image_files[0])
    target_size = first_img.size
    valid_images = [img for img in image_files if Image.open(img).size == target_size]

    if not valid_images:
        print("No images matched the target resolution.")
        return

    num_images = len(valid_images)
    full_rows = num_images // columns  # only complete rows
    total_images = full_rows * columns  # ignore leftover images

    if total_images == 0:
        print(f"Not enough images to fill one complete row of {columns} columns.")
        return

    rows = full_rows
    width, height = target_size
    collage_w = columns * width
    collage_h = rows * height

    collage = Image.new('RGBA', (collage_w, collage_h), bg_color)

    for i in range(total_images):
        img_path = valid_images[i]
        img = Image.open(img_path)
        row = i // columns
        col = i % columns
        x = col * width
        y = row * height
        collage.paste(img, (x, y))

    if blur_strength > 0:
        collage = collage.filter(ImageFilter.GaussianBlur(radius=blur_strength))
        print(f"Applied Gaussian blur with strength {blur_strength}")

    collage.save(output_file)
    print(f"Collage saved to {output_file} with {total_images} images in {columns} columns x {rows} full rows.")

# Example usage:
make_collage_full_rows("input", output_file="collage.png", columns=5, blur_strength=20)
