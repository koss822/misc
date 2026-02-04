from rembg import remove
from PIL import Image
import sys
import io


def remove_bg(input_path, output_path):
    """
    Removes the background from an image and saves the output.
    """
    # Load image as bytes
    with open(input_path, 'rb') as i:
        input_data = i.read()
    
    # Remove background
    output_data = remove(input_data)
    
    # Save output
    with open(output_path, 'wb') as o:
        o.write(output_data)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python remove_bg.py input.jpg output.png")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    remove_bg(input_file, output_file)
    print(f"Background removed: {output_file}")
