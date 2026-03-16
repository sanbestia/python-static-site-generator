import os
import shutil
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def check_dir(dir):
    if not os.path.exists(dir):
        raise Exception(f'Error: source directory \'./{dir}\' not found')
    if os.path.isfile(dir):
        raise Exception(f'Error: \'./{dir}\' is a file')

    
def copy_dir_content_r(source_dir, target_dir):
    for elem in os.listdir(source_dir):
        elem_path = os.path.join(source_dir, elem)
        if os.path.isfile(elem_path):
            logger.info(f'copying file \'{elem_path}\' contents to dir \'{target_dir}\'...')
            shutil.copy(elem_path, target_dir)
        if os.path.isdir(elem_path):
            target_dir_path = os.path.join(target_dir, elem)
            logger.info(f'creating dir \'{target_dir_path}\'...')
            os.mkdir(target_dir_path)
            logger.info(f'copying dir \'{elem_path}\' contents to dir \'{target_dir_path}\'...')
            copy_dir_content_r(elem_path, target_dir_path)
            

def copy_dir_content(source_dir, target_dir):
    if source_dir == target_dir:
        raise Exception('Can\'t copy a directory into itself')
    
    wd = os.getcwd()
    full_source_dir = os.path.join(wd, source_dir)
    try:
        check_dir(full_source_dir)
    except Exception as e:
        logger.error(e)
        return
    
    full_target_dir = os.path.join(wd, target_dir)
    logger.info(f'copying dir \'{full_source_dir}\' contents to dir \'{full_target_dir}\'...')

    # Clean new_dir by erasing it
    if os.path.exists(full_target_dir):
        logger.info(f'removing dir \'{full_target_dir}\' and all of its contents...')
        shutil.rmtree(full_target_dir)
    
    # Create target dir
    logger.info(f'creating dir \'{full_target_dir}\'...')
    os.mkdir(full_target_dir)
          
    # Copy source dir into target_dir
    copy_dir_content_r(full_source_dir, full_target_dir)