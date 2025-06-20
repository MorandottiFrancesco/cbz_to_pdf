#place images in folder with a number 

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import glob
import re

def create_pdf(image_paths, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    for image_path in image_paths:
        img = Image.open(image_path)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        c.setPageSize((letter[0], letter[0] * aspect))
        c.drawImage(image_path, 0, 0, width=letter[0], height=letter[0] * aspect)
        c.showPage()
    c.save()

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List all subdirectories in the script directory
    subdirs = [d for d in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(script_dir, subdir)

        # Extract the full number from the subdirectory name
        match = re.search(r'\d+', subdir)
        if match:
            number = match.group()
            pdf_path = os.path.join(script_dir, f'{number}.pdf')

            # Use glob to find all .jpg and .png files in the subdirectory
            image_paths = glob.glob(os.path.join(subdir_path, '*')) #'RCO*_*.*'

    def get_sort_key(path):
        # Extract the filename from the path
        filename = os.path.basename(path)

        # Use regular expression to find any number between two underscores
        match = re.search(r'_(.*?)_', filename)

        if match:
            # Extract the number and convert it to an integer
            num = int(match.group(1))
            return num
        else:
            # Return a default value if no number is found
            return 0


            # Filter and sort the image paths based on the 3-digit number
            def get_sort_key2(path):
                # Extract the 3-digit number from the filename
                filename = os.path.basename(path)
                num = int(filename.split('_')[0][3:])  # Extract the number after 'RCO'
                return num

            image_paths = sorted(image_paths, key=get_sort_key)

            # Create PDF
            create_pdf(image_paths, pdf_path)
            print(f"PDF created successfully at {pdf_path}")

if __name__ == '__main__':
    main()
