from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import re
import glob
import traceback

def create_pdf(image_paths, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    for image_path in image_paths:
        try:
            if os.path.exists(image_path) and os.path.isfile(image_path):
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
                    aspect = img_height / float(img_width)
                    c.setPageSize((letter[0], letter[0] * aspect))
                    c.drawImage(image_path, 0, 0, width=letter[0], height=letter[0] * aspect)
                    c.showPage()
            else:
                print(f"File not found or is not a file: {image_path}")
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            traceback.print_exc()
    c.save()

def main():
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Use glob to find all .jpg and .png files in the script directory
        image_paths = glob.glob(os.path.join(script_dir, '*.jpg')) + glob.glob(os.path.join(script_dir, '*.png'))
        print(script_dir)

        # Filter and sort the image paths based on the last number in the filename
        def get_sort_key(path):
            # Extract the last number from the filename
            filename = os.path.basename(path)
            # Find all sequences of digits in the filename
            numbers = re.findall(r'\d+', filename)
            print(filename)
            if numbers:
                # Extract the last number and convert it to an integer
                last_number = int(numbers[-1])
                print(last_number)

                return last_number

            else:
                return 0

        image_paths = sorted(image_paths, key=get_sort_key)

        # Output PDF path
        pdf_path = os.path.join(script_dir, 'output.pdf')

        # Create PDF
        create_pdf(image_paths, pdf_path)
        print(f"PDF created successfully at {pdf_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()
