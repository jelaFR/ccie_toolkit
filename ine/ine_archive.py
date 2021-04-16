import zipfile
import re
import os
from sys import platform


class INEArchive:
    """
    Represent INE archive file composed with multiple configuration files organized this way:
        Level 1 : Root
        ->  Level 2 : LAB Type
            -> Level 3 : LAB name
    """

    def __init__(self, archive_name):
        """
        Initiate INE ZIP Archive containing multiple LAB configurations located in folders and subfolders

        Args:
            archive_name (str): Full path to INE workbook archive file (.zip file)
        """
        self.archive_name = archive_name


    def lab_selector(self):
        # Display menu for categories
        lab_tree = list(self._get_lab_tree())
        # Check if categories exist
        if len(lab_tree) != 0:
            while True:
                self._clear_screen()
                for cat_id, category_name in enumerate(lab_tree, start=1):
                    print(f"{cat_id}. {category_name}")
                lab_category = input(f"Please select LAB category [1-{len(lab_tree)}]: ")
                try:
                    lab_category = lab_tree[int(lab_category)-1]
                    break
                except:
                    input(f"[ERROR] You type : {lab_category}, we expect an integer between 1 and {len(lab_tree)}")
        else:
            print(f"[ERROR] Unable to get category list inside {self.archive_name}")

        # Display menu for labs
        lab_tree = list(self._get_lab_tree()[lab_category])
        # Check if labs exists inside archive
        if len(lab_tree) != 0:
            while True:
                for lab_id, lab_name in enumerate(lab_tree, start=1):
                    print(f"{lab_id}. {lab_name}")
                lab_name = input(f"Please select LAB name [1-{len(lab_tree)}]: ")
                try:
                    lab_name = lab_tree[int(lab_name)-1]
                    break
                except:
                    input(f"[ERROR] You type : {lab_name}, we expect an integer between 1 and {len(lab_tree)}")
        else:
            print(f"[ERROR] Unable to get lab list inside {self.archive_name}")

        project_files = self._get_lab_tree(category_filter=lab_category, lab_filter=lab_name)

        return project_files


    def _clear_screen(self):
        """
        Clear displayed infos on screen
        """
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            os.system('clear')
        elif platform == "win32":
            os.system('cls')


    def _get_lab_tree(self, category_filter="", lab_filter=""):
        """
        Provides a tree for labs contained in the Zip Archive

        Args:
            category_filter (str, optional): Returns only categories matching this expression. Defaults to "".
            lab_filter (str, optional): Returns only lab matching this expression. Defaults to "".

        Returns:
            dict: Tree of categories, labs and files contained in the Zip Archive
            "LAB_CATEGORY_1":
                {
                "LAB_NAME_1":
                    [
                    ("hostname","LAB_FILE_1"),
                    ("hostname_2","LAB_FILE_2"),
                    ("hostname_3",LAB_FILE_3")
                    ]
                }
            "LAB_CATEGORY_2":
                {
                "LAB_NAME_1":
                    [
                    "LAB_FILE_1",
                    "LAB_FILE_2",
                    "LAB_FILE_3"
                    ]
                }
        """
        lab_tree = dict()
        re_category = re.compile(category_filter)
        re_lab = re.compile(lab_filter)
        # Open ZIP archive
        with zipfile.ZipFile(self.archive_name) as zip_file:
            for lab_files in self._get_files():
                root, lab_category, lab_name, lab_file = lab_files.split("/")
                if re_category.match(lab_category) and re_lab.match(lab_name):
                    # Create lab category in Tree
                    if not lab_tree.get(lab_category) :
                        lab_tree[lab_category] = dict()
                    # Create lab name in Tree
                    if not lab_tree[lab_category].get(lab_name):
                        lab_tree[lab_category][lab_name] = list()
                    # Put all devices in lab name
                    router_cfg = self._get_file_content(zip_file, lab_files)
                    if lab_file.endswith(".txt"):
                        router_name = lab_files.split(".")[0]
                    router_name = lab_file
                    lab_tree[lab_category][lab_name].append((router_name, router_cfg))
        return lab_tree


    def _get_dirs(self, dir_filter=""):
        """
        Provides list of directories containted in the archive

        Args:
            dir_filter (str, optional): Returns only directories matching filter. Defaults to "".

        Returns:
            list: List of directories contained in the Zip archive
        """
        dir_list = list()
        filter_re = re.compile(dir_filter)
        if self._is_valid():
            # Get a list of all files in the zip archive
            for dir_names in zipfile.ZipFile(self.archive_name).infolist():
                # Collect only directory / Collect only directories matching REGEXP
                if dir_names.is_dir() and filter_re.search(dir_names.filename):
                    dir_list.append(dir_names.filename)
        return dir_list


    def _get_files(self, file_filter=""):
        """
        Provides list of files containted in the archive

        Args:
            file_filter (str, optional): Returns only files matching filter. Defaults to "".

        Returns:
            list: List of files contained in the Zip archive
        """
        file_list = list()
        filter_re = re.compile(file_filter)
        if self._is_valid():
            # Get a list of all files in the zip archive
            for file_name in zipfile.ZipFile(self.archive_name).infolist():
                # Collect only files / Collect only files matching REGEXP
                if not file_name.is_dir() and filter_re.search(file_name.filename):
                    file_list.append(file_name.filename)
        return file_list


    def _get_file_content(self, zip_file, filename):
        """
        Provides content of a file inside zip archive

        Args:
            filename (str): Extract the content of this file.

        Returns:
            str: Content of archive encoded in UTF-8. Returns False if decode fails.
        """
        with zip_file.open(filename) as myfile:
            archive_content = myfile.read()
            try:
                archive_content.decode('UTF-8')
            except:
                archive_content = False
        return archive_content


    def _is_valid(self):
        """
        Check if ZIP file is a valid ZIP file

        Returns:
            (bool): True if file is a valid zip file, False if not.
        """
        if zipfile.is_zipfile(self.archive_name):
            # TODO : Check INE CCIE Enterprise file and check if structure is consistent with INE R&S v5.1
            return True
        return False
