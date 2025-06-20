import os
import zipfile
from PIL import Image

def extract_cbz(cbz_file, extract_to):
    """Extracts the CBZ file (ZIP) to the specified folder."""
    with zipfile.ZipFile(cbz_file, 'r') as cbz:
        cbz.extractall(extract_to)
    print(f"Extracted {cbz_file} to {extract_to}")

def create_pdf_from_images(images_folder, output_pdf):
    """Creates a PDF file from images in the folder."""
    image_files = sorted(os.listdir(images_folder))  # Sort files by name
    image_list = []
    
    # Open images and append to the list
    for image_file in image_files:
        image_path = os.path.join(images_folder, image_file)
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(image_path)
            # Convert to RGB mode if necessary (for PNGs with alpha channels)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            image_list.append(img)

    # Ensure there's at least one image
    if len(image_list) > 0:
        # Save all images into a single PDF
        image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
        print(f"PDF created: {output_pdf}")
    else:
        print("No valid images found in the folder.")

def cbz_to_pdf(cbz_file, output_pdf):
    """Converts a CBZ file to PDF format."""
    # Step 1: Create a temporary directory to extract the CBZ
    temp_dir = 'D:\\d3\\daniel way\\cbz to epub\\temp_cbz_extract' 
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Step 2: Extract the CBZ file
    #extract_cbz(cbz_file, temp_dir)

    # Step 3: Create the PDF from extracted images
    create_pdf_from_images(temp_dir, output_pdf)

    # Step 4: Clean up temporary files (optional)
    #for file in os.listdir(temp_dir):
    #    os.remove(os.path.join(temp_dir, file))
    #os.rmdir(temp_dir)
    #print(f"Temporary files cleaned up.")

# Example usage
cbz_file_path = 'D:\\d3\\daniel way\\cbz to epub\\example.cbz'
output_pdf_path = 'D:\\d3\\daniel way\\cbz to epub\\output.pdf'

cbz_to_pdf(cbz_file_path, output_pdf_path)
