#!/usr/bin/env python3

"""Docstring for jpg2png.py module.
Summary
-------
    The script called 'jpg2png' aims to convert jpg-files to png-files,
    the modules does this by accepting a source/root directory with jpg-files
    and creating a new directory.

Functions
---------
    'is_dir',
    '_filter_jpg',
    'is_file_jpg',
    'load_jpgs',
    'make_dir',
    'jpg2png',
    'main'

Examples
--------
    To run script
    'python jpg2png ./source_dir target'

    To run script using python shebang
    'chmod +x ./jpg2png.py'
    './jpg2png ./source_dir target'
"""

from pathlib import Path
from PIL import Image
from argparse import ArgumentParser


def is_dir(dir_name: str):
    """The 'is_dir' converts string input to a directory

    Parameters
    ----------
    dir_name : str
        The 'dir_name' set path to directory

    Returns
    -------
    root_dir : Path.object
        The 'root_dir' is the path to directory with validation checked.

    bool
        If the path has failed validation. The value is set to 'False'.

    Raises
    ------
    AssertionError
        if 'dir_name' not str typed.

    See Also
    --------
    pathlib.Path.is_dir : For more information of directory validation.
    pathlib.Path: For more information about regarding file and directory
    creation.
    """
    try:
        assert isinstance(dir_name, str), "Parameter 'dir_name' must be str"

    except AssertionError as error:
        raise ValueError(f"{error}")
    else:
        root_dir = Path.cwd() / dir_name

        if not root_dir.is_dir():
            return False

        return root_dir


def _filter_jpg(file_name):
    """Helper function that determines if a file is a jpg or not

    Parameters
    ----------
    file_name : str
    The 'file_name' is absolute or relative path from cwd.

    Returns
    -------
    bool
        If the 'file_name' ends with '*.jpg'

    See Also
    --------
    jpg2png.is_file_jpg : To see where helper function is implemented.
    """
    if str(file_name).endswith(".jpg"):
        return True
    return False


def is_file_jpg(path_to_dir: str):
    """
    The function loops through a directory in search of jpg-file.

    Parameters
    ----------
    path_to_dir : str
        The 'path_to_dir' parameter is the relative or absolute path to a
        source directory with jpg-files.

    Returns
    -------
    all_jpgs
        The return value 'all_jpgs' is a list object with items, where each
        item points to a file that ends with '.jpg'.
    bool
        Otherwise the return values is 'bool' set to 'False'.

    Raises
    ------
    AssertionError
        If directory has no jpg-files in it.

    AttributeError
        If path to directory is invalid or faulty.
    """

    dir_path = is_dir(dir_name=path_to_dir)
    try:
        jpgs = filter(_filter_jpg, dir_path.iterdir())
        if not jpgs:
            raise AssertionError("No jpgs were found in directory")
    except AttributeError:
        print("Path of directory was invalid")
        return False
    except AssertionError as error:
        print(error)
        return False

    else:
        all_jpgs = [pic for pic in jpgs]
        return all_jpgs


def load_jpgs(file_paths_to_jpg: list):
    """
    The function loads jpg-files to PIL.Image object.
    Parameters
    ----------
    file_paths_to_jpg : list
        The 'file_paths_to_jpg' is list populated with strings that point to
        jpg-files.

    Returns
    -------
    jpg_images
        The return value 'jpg_images' is list populated with
        PIL.Image.open(item).

    Raises
    ------
    AttributeError
        If 'file_paths_to_jpgs' is not a proper pathlib.Path object.
        Return value is set to False.

    """
    img = Image
    try:
        file_paths_to_jpg[0].is_file()
    except AttributeError as error:
        print(f"Missing jpg: {error}")
        return False
    else:
        jpg_images = [img.open(pic_name.absolute()) for pic_name in
                      file_paths_to_jpg]
        return jpg_images


def make_dir(path_to_dir: str):
    """
    The function creates directories with pathlib.Path.mkdir().
    Parameters
    ----------
    path_to_dir: str
        The 'path_to_dir' is the absolute or real path from cwd to creation
        of location.

    Returns
    -------
    new_dir: Path.mkdir()
    The 'new_dir' is the object created from pathlib.Path.mkdir().

    Raises
    ------
    FileNotFoundError
        if 'new_dir' stem part of 'directory path' is nonexistent or invalid.

    FileExistsError
        if 'new_dir' path exists already.

    See Also
    --------
    pathlib.Path.mkdir: For more information on directory creation.

    """
    new_dir = Path().cwd() / path_to_dir
    try:
        new_dir.mkdir()
    except FileNotFoundError as error:
        print(f"Path to new dir was invalid: {error}")
        return False

    except FileExistsError:
        print("Directory already exits!")
        return new_dir

    else:
        print(f"Directory was created at: {new_dir.absolute()}")
        return new_dir


def jpg2png(path_to_jpgs: list, new_location: str):
    """
    This function takes a jpg-file and converts it to png.
    Parameters
    ----------
    path_to_jpgs : list
        The 'path_to_jpgs' are the absolute or relative path to a jpg-file
        from current working directory (cwd). The 'path_to_jpgs' is a list
        object with items that are str that lead to a single jpg-file.

    new_location: str
        The 'new_location' is the relative or absolute path from cwd to a
        nonexistent directory.

    Returns
    -------
    converted
        If jpgs-files are converted, return value 'converted' is set to True.
    Bool
        If jpgs-file are not converted. The value is set to False.

    """
    new_dir = make_dir(new_location)
    try:
        png_name = [new_dir.joinpath(pic.name.replace(".jpg", ".png"))
                    for pic in path_to_jpgs]
    except (TypeError, AttributeError):
        return new_dir
    else:
        jpgs = load_jpgs(file_paths_to_jpg=path_to_jpgs)

        png_pics = [pic.save(png_name[i], "png") for i, pic in enumerate(
                jpgs)]
        converted = all([True for pic in png_pics if pic is None])
        return converted


def main(root_dir, new_dir):
    """
    The recipe function  for conversion of jpgs to pngs.

    Parameters
    ----------
    root_dir : str
        The 'root_dir' relative or absolute from cwd to source directory with
        jpgs files.

    new_dir: str
        The 'new_dir' the location from cwd to new directory.

    Returns
    -------
    None

    See Also
    --------
    jpg2png : For more information of expected outcomes.

    """
    all_jpgs = is_file_jpg(root_dir)
    if all_jpgs:
        all_png = jpg2png(path_to_jpgs=all_jpgs, new_location=new_dir)
        return all_png
    else:
        return all_jpgs


if __name__ == "__main__":
    dir_names = ArgumentParser(description="The directory names for jpg2png "
                                           "conversion")
    dir_names.add_argument(
        "source_dir", type=str, nargs="?", default=str(Path.cwd().absolute()),
        help="The path to the directory with jpg-files")
    dir_names.add_argument(
        "target_dir", type=str, nargs="?", default="./new_pngs",
        help="The directory path to store converted jpg-files")
    dir_paths = dir_names.parse_args()

    main(root_dir=dir_paths.source_dir, new_dir=dir_paths.target_dir)

