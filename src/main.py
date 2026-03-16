from file_functions import copy_dir_content
import os


def main():
    root_dir = os.path.abspath('.')
    static_dir = os.path.join(root_dir, 'static/')
    public_dir = os.path.join(root_dir, 'public/')
    copy_dir_content(static_dir, public_dir)
    
    
if __name__ == '__main__':
    main()