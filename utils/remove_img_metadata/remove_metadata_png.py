import os
from PIL import Image

def remove_metadata_from_png_folder(input_dir="input", output_dir="output"):
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    png_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]
    if not png_files:
        print("No PNG files found in the input directory.")
        return

    for filename in png_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        try:
            with Image.open(input_path) as img:
                img = img.convert("RGBA") if img.mode in ("P", "LA") else img.convert(img.mode)
                img.save(output_path, "PNG", optimize=True)
                print(f"Processed: {filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    remove_metadata_from_png_folder()
