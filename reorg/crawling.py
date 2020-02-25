"""Functions needed during the crawling of the source directory"""
import os


def should_create_page(step):
    _, _, files = step
    return "_index.md" in files

def is_name_special(name_to_check):
    return name_to_check[0] == "_"

def is_path_special(dir_root, dir_to_check):
    common = os.path.commonpath([dir_root, dir_to_check])
    dtc = dir_to_check.replace(common, "")
    print(os.path.split(dtc))

    while True:
        # This loop terminates when there's no more in the path to pop off
        # i.e. ('/', '')
        (dtc, tail) = os.path.split(dtc)
        if tail:
            if is_name_special(tail):
                # If any part is special then True
                return True
        else:
            break
    return False

# REVIEW: Death watch - is this func needed?
def is_leaf_node(step):
    _, dir_names, _ = step
    # All dirs that start with underscore are special
    dir_names = [d for d in dir_names if not is_name_special(d)]
    return True if len(dir_names) == 0 else False

def whats_target_dir_for_section(dir_curr_crawl, dir_src, dir_target):
    """Determine the target directory that the current section should be copied to"""
    # TODO: Create dir_target where dir_target + (dir_curr - dir_src) without
    # basename
    # Maybe start with dir_target + (dir_curr - dir_src) then chop off basename
    dir_rel = dir_curr_crawl.replace(
            os.path.commonpath([dir_curr_crawl, dir_src]), "")

    if dir_rel:
        dir_rel = dir_rel[1:] if dir_rel[0] == "/" else dir_rel
        return os.path.join(dir_target, dir_rel)
    else:
        # You are here because dir_curr_crawl and dir_src are the same
        return dir_target
