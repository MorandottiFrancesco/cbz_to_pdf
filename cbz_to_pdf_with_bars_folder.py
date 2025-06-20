import os
import zipfile
from PIL import Image

def extract_cbz(cbz_file, extract_to):
    """Extracts the CBZ file (ZIP) to the specified folder."""
    with zipfile.ZipFile(cbz_file, 'r') as cbz:
        cbz.extractall(extract_to)
    print(f"Extracted {cbz_file} to {extract_to}")

def resize_and_pad_image(image, target_size):
    """
    Resizes an image to fit within target_size (2160x1620),
    while maintaining aspect ratio, and pads with black bars.
    """
    # Get the original image size
    original_width, original_height = image.size

    # Target size for the image
    target_width, target_height = target_size

    # Calculate the aspect ratio of the original image
    aspect_ratio = original_width / original_height

    # Calculate the new size, maintaining aspect ratio
    if aspect_ratio > (target_width / target_height):
        # Image is wider in aspect, so resize based on the width
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        # Image is taller in aspect, so resize based on the height
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Create a new black background image with the target size
    padded_image = Image.new("RGB", target_size, (0, 0, 0))

    # Calculate position to center the resized image on the black background
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2

    # Paste the resized image onto the black background
    padded_image.paste(resized_image, (offset_x, offset_y))

    return padded_image

def create_pdf_from_images(images_folder, output_pdf, target_size=(1620, 2160)):
    """Creates a PDF file from images in the folder, ensuring each page is 2160x1620 with black padding."""
    image_files = sorted(os.listdir(images_folder))  # Sort files by name
    image_list = []
    
    # Open images, resize, pad, and append to the list
    for image_file in image_files:
        image_path = os.path.join(images_folder, image_file)
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(image_path)
            
            # Convert to RGB mode if necessary (for PNGs with alpha channels)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize and pad the image
            resized_img = resize_and_pad_image(img, target_size)
            image_list.append(resized_img)

    # Ensure there's at least one image
    if len(image_list) > 0:
        # Save all images into a single PDF
        image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
        print(f"PDF created: {output_pdf}")
    else:
        print("No valid images found in the folder.")

def cbz_to_pdf(cbz_file, output_pdf):
    """Converts a CBZ file to PDF format with each page being 2160x1620 pixels."""
    # Step 1: Create a temporary directory to extract the CBZ
    temp_dir = 'temp_cbz_extract'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Step 2: Extract the CBZ file
    extract_cbz(cbz_file, temp_dir)

    # Step 3: Create the PDF from extracted images
    #create_pdf_from_images(temp_dir, output_pdf)

    # Step 4: Clean up temporary files (optional)
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
    print(f"Temporary files cleaned up.")

def process_all_cbz_in_folder(folder_path, output_folder):
    """Processes all .cbz files in the specified folder and converts them to PDFs."""
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all .cbz files in the folder
    for cbz_file in os.listdir(folder_path):
        if cbz_file.endswith('.cbz'):
            cbz_file_path = os.path.join(folder_path, cbz_file)
            output_pdf_name = os.path.splitext(cbz_file)[0] + '.pdf'  # Same name but with .pdf extension
            output_pdf_path = os.path.join(output_folder, output_pdf_name)

            print(f"Processing: {cbz_file_path}")
            cbz_to_pdf(cbz_file_path, output_pdf_path)

# Example usage
input_folder = 'D:\\d3\\daniel way\\cbz to epub\\input'       # Folder containing .cbz files
output_folder = 'pdf_output'     # Folder to save the converted PDF files

process_all_cbz_in_folder(input_folder, output_folder)
