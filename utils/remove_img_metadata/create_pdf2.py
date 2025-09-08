from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

input_folder = 'input'
output_pdf = 'output2.pdf'
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

# A4 page size in points (1 point = 1/72 inch)
PAGE_WIDTH, PAGE_HEIGHT = A4

# Get sorted image files
image_files = [
    os.path.join(input_folder, f)
    for f in sorted(os.listdir(input_folder))
    if f.lower().endswith(image_extensions)
]

if not image_files:
    print("No image files found.")
    exit()

# Create PDF
c = canvas.Canvas(output_pdf, pagesize=A4)

for img_path in image_files:
    img = Image.open(img_path)
    img_width, img_height = img.size

    # Scale to fit within A4 page
    scale = min(PAGE_WIDTH / img_width, PAGE_HEIGHT / img_height)
    new_width = img_width * scale
    new_height = img_height * scale

    # Center the image
    x = (PAGE_WIDTH - new_width) / 2
    y = (PAGE_HEIGHT - new_height) / 2

    # Convert to ImageReader object
    img_reader = ImageReader(img)

    # Draw image
    c.drawImage(img_reader, x, y, width=new_width, height=new_height)

    c.showPage()  # Next page

c.save()
print(f"PDF created: {output_pdf}")
