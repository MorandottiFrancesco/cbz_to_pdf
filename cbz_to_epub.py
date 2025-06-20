import os
import zipfile
from PIL import Image
from ebooklib import epub

def extract_cbz(cbz_file, extract_to):
    """Extracts the CBZ file (ZIP) to the specified folder."""
    with zipfile.ZipFile(cbz_file, 'r') as cbz:
        cbz.extractall(extract_to)
    print(f"Extracted {cbz_file} to {extract_to}")

def create_epub_from_images(images_folder, output_epub):
    """Creates an EPUB file from images in the folder."""
    book = epub.EpubBook()

    # Set metadata for the EPUB book
    book.set_identifier('1')
    book.set_title('Deadpool by Daniel Way: The Complete Collection Vol1')
    book.set_language('en')

    # Add a cover image if there is one (first image used as cover)
    image_files = sorted(os.listdir(images_folder))  # Sort files by name
    if len(image_files) > 0:
        first_image_path = os.path.join(images_folder, image_files[0])
        book.set_cover("cover.jpg", open(first_image_path, 'rb').read())

    # Add each image file as an item in the EPUB
    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(images_folder, image_file)
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            img = open(image_path, 'rb').read()
            img_item = epub.EpubItem(
                uid=f"img{idx}",
                file_name=f"image{idx}.jpg",
                media_type="image/jpeg",
                content=img
            )
            book.add_item(img_item)

            # Create an HTML page for each image
            page = f'<html><body><img src="image{idx}.jpg" alt="comic image"/></body></html>'
            chapter = epub.EpubHtml(title=f'Page {idx + 1}', file_name=f'page_{idx}.xhtml', content=page)
            chapter.add_item(img_item)
            book.add_item(chapter)

    # Create table of contents
    book.toc = [epub.Link(f'page_{idx}.xhtml', f'Page {idx + 1}', f'page_{idx}') for idx in range(len(image_files))]

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define the spine of the book (order of contents)
    book.spine = ['cover'] + [f'page_{idx}' for idx in range(len(image_files))]

    # Write to the output EPUB file
    epub.write_epub(output_epub, book)
    print(f"EPUB created: {output_epub}")

def cbz_to_epub(cbz_file, output_epub):
    """Converts a CBZ file to EPUB format."""
    # Step 1: Create a temporary directory to extract the CBZ
    temp_dir = 'D:\\d3\\daniel way\\cbz to epub\\temp_cbz_extract' 
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Step 2: Extract the CBZ file
    #extract_cbz(cbz_file, temp_dir)

    # Step 3: Create the EPUB from extracted images
    create_epub_from_images(temp_dir, output_epub)

    # Step 4: Clean up temporary files (optional)
    #for file in os.listdir(temp_dir):
    #    os.remove(os.path.join(temp_dir, file))
    #os.rmdir(temp_dir)
    #print(f"Temporary files cleaned up.")

# Example usage
cbz_file_path = 'D:\\d3\\daniel way\\cbz to epub\\example.cbz'
output_epub_path = 'D:\\d3\\daniel way\\cbz to epub\\output.epub'
#cbz_file_path = 'example.cbz'  # Path to your CBZ file
#output_epub_path = 'output.epub'  # Path to save the converted EPUB

cbz_to_epub(cbz_file_path, output_epub_path)