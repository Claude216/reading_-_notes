import os

def rename_files(folder_path, new_prefix):
    """Renames all files in a folder by adding a prefix to their names.

    Args:
        folder_path: The path to the folder containing the files to rename.
        new_prefix: The prefix to add to the beginning of each filename.
    """
    for filename in os.listdir(folder_path):
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_prefix + filename)
        os.rename(src, dst)


folder_path = "./0_derived_papers/"
new_prefix = "1_"

rename_files(folder_path=folder_path, new_prefix=new_prefix)