import os
from pathlib import Path
from PIL import Image
from tensorflow.keras.preprocessing import image

def convert_tiff_to_jpeg(img_path, out_dir):
    """
    Creates the .jpeg version of the .tiff file.
    """
    uploads_folder = Path(img_path).parents[0]
    base_name = Path(img_path).stem
    outfile = os.path.join(out_dir, f"{base_name}.jpg")
    bgfile = os.path.join(uploads_folder, f"{base_name}_bg.jpg")

    if os.path.isfile(outfile):
        print(f"A jpeg file already exists for {outfile}")
    else:
        img = image.load_img(img_path, target_size=(400, 400), color_mode="rgb")
        # img.load()
        # background = Image.new("RGB", img.size, (255, 255, 255))
        # background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
        # background.save(bgfile, "JPEG", quality=100)
        # img.thumbnail(im.size)
        # format: JPEG
        img.save(outfile, "JPEG", quality=100)

if __name__ == "__main__":
    from tqdm import tqdm
    from glob import glob

    # change the paths to your files here!
    blast_files = glob(r"C:\Users\jchen\Desktop\MIT Hackathon\blast_cells\*.tiff",
                       recursive=True)
    non_malig_files = glob(r"C:\Users\jchen\Desktop\MIT Hackathon\non_malignant\*.tiff",
                           recursive=True)

    for tiff_path in tqdm(blast_files):
        convert_tiff_to_jpeg(tiff_path, r"C:\Users\jchen\Desktop\MIT Hackathon\blast_cells_jpeg")

    for tiff_path in tqdm(non_malig_files):
        convert_tiff_to_jpeg(tiff_path, r"C:\Users\jchen\Desktop\MIT Hackathon\non_malignant_jpeg")
