from PIL import Image
import os

# Folder containing input images
input_folder = 'input'
output_pdf = 'output.pdf'

# Supported image extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

# Collect all image file paths
image_files = [
    os.path.join(input_folder, f)
    for f in sorted(os.listdir(input_folder))
    if f.lower().endswith(image_extensions)
]

if not image_files:
    print("No image files found in the 'input' folder.")
    exit()

# Open images and convert to RGB (PDF requires RGB)
images = [Image.open(img_path).convert('RGB') for img_path in image_files]

# Save as a single PDF
images[0].save(output_pdf, save_all=True, append_images=images[1:])

print(f"PDF created successfully: {output_pdf}")
