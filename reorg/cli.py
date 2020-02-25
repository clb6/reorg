import sys, os, shutil
from datetime import datetime as dt
from reorg import page
from reorg import crawling as cr


def adjust_target_dir_for_page(dir_target):
    """From path to directory target as if for section"""
    basename = os.path.basename(dir_target)
    return dir_target.replace(basename, "")


def whats_dir_target(dir_target_user):
    """Determine the target directory root path to be used"""
    dir_target_default = os.environ["PWD"]
    dir_target = dir_target_user if dir_target_user else dir_target_default
    return os.path.join(dir_target, "reorged")

def prepare_dir_target(dir_target):
    if os.path.exists(dir_target):
        # TODO: Need user prompt
        shutil.rmtree(dir_target)
        print("Purged previous target \"{0}\"".format(dir_target))

    os.mkdir(dir_target)
    print("Created target \"{0}\"".format(dir_target))


def run():
    dir_src_root = sys.argv[1].rstrip(os.sep)
    print("Reorganizing \"{0}\"".format(dir_src_root))
    dir_target_root = whats_dir_target(sys.argv[2] if len(sys.argv) > 2 else None)
    prepare_dir_target(dir_target_root)

    # Step is ("/current-directory", ["sub-directory"], ["some-file"])
    for step in os.walk(dir_src_root):
        print(step)
        dir_curr, dirs_in_curr, files_in_curr = step

        if cr.is_path_special(dir_src_root, dir_curr):
            print("Skipping special directory")
        elif cr.should_create_page(step):
            dir_target = cr.whats_target_dir_for_section(dir_curr, dir_src_root,
                    dir_target_root)

            # Give up on being slick by trying to avoid creating top-level
            # sectional/group directory. Assume contexts/concepts will most likely
            # have some directory to be copied anyways, code will be simpler..

            # Handling _pages must be first since it requires that the directory
            # doesn't already exist
            # TODO: Inject TOC into index page
            if "_pages" in dirs_in_curr:
                src = os.path.join(dir_curr, "_pages")
                # NOTE: Copying into top-level group directory
                dest = dir_target
                shutil.copytree(src, dest)

            # Straight up copy _static
            # TODO: Should _static dirs be merged in a big global dir?
            if "_static" in dirs_in_curr:
                src = os.path.join(dir_curr, "_static")
                dest = os.path.join(dir_target, "static")
                shutil.copytree(src, dest)

            # Handle index and notes
            if not os.path.exists(dir_target):
                os.mkdir(dir_target)

            page_text = page.create_page(step)
            page_path = os.path.join(dir_target, page.create_page_name(dir_curr))

            with open(page_path, "w+") as f:
                f.write(page_text)
        else:
            # Just create a directory
            dir_target = cr.whats_target_dir_for_section(dir_curr, dir_src_root,
                    dir_target_root)

            if not os.path.exists(dir_target):
                os.mkdir(dir_target)
