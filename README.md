The main and most complete variant of the scripts is the cbz_to_pdf_bars_folder. It features a middle step to allow re-organizing the single images in a folder before compiling the pdf.
Images are resized to 2160x1620 adding horizontal or vertical bars in order to match the target resolution size even when the starting image has a different form factor. 
This improves readability on the ReMarkable Paper Pro, which supports colors and can therefore be used as cool comic book reader. By resizing to the native resolution the pages need less loading time, giving a more fluid reading experience, furthermore the battery life is prolonged since the pages need not be resized by the device before they are displayied.


image_to_pdf and image_to_pdf_general also have a similar function, in that they take pictures downloaded from the internet and placed in a folder and stich together a pdf file. In this case the script looks for any kind of numbering system in the filenames and will try to match the order of the pages to those numbers - if available. 
