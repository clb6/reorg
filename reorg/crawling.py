"""Functions needed during the crawling of the source directory"""
import os


def should_create_page(step):
    _, _, files = step
    return "_index.md" in files

def is_name_special(name_to_check):
    return name_to_check[0] == "_"

def is_path_special(dir_to_check):
    name = os.path.basename(dir_to_check)
    return is_name_special(name)

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
