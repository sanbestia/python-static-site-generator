from html_functions import generate_pages_recursively
from file_functions import copy_dir_content
import sys
import os


def main(): 
    basepath = '/'
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    root_dir = os.path.abspath('.')
    
    static_dir = os.path.join(root_dir, 'static/')
    public_dir = os.path.join(root_dir, 'public/')
    copy_dir_content(static_dir, public_dir)
    
    
    from_path = os.path.join(root_dir, 'content/')
    template_path = os.path.join(root_dir, 'template.html')
    dest_path = os.path.join(root_dir, 'public/')
    generate_pages_recursively(from_path, template_path, dest_path, basepath)
    
    
if __name__ == '__main__':
    main()