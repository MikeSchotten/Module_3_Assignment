__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"


import os
import shutil
import pathlib


# ---------------NOTE TO INSTRUCTORS--------------------------
#
# I made this extra function below to ensure that the path always returns
# to the ../Winc/files/ folder, i.e. the folder where the file
# 'main.py' is located and is operating from.  This is bcs. I ran into problems with
# the WincPy check: while everything worked fine (all 4 functions
# in the assignment) when I ran main.py myself in Thonny, at first WincPy (which I run from VS Codium)
# didn't pass the check for one or several of the 4 functions, and this kept
# changing unpredictably (sometimes the first 3 would pass, sometimes some of them wouldn't, etc.)
#
# I read in the Data Analytics forum that a few other people had the same kind of problems,
# and I suspected a potential bug in the WincPy checking code.  After much
# trouble-shooting (by using print(path) statements inside the 4 functions),
# I discovered that a change of path inside the functions is the culprit;
# e.g., inside the cached_files() function, it changes the path to the ../cache folder,
# and if it would STAY there, this can cause problems down the line, when
# other functions such as clean_cache() are called again in WincPy.  It happened to me a few
# times during the WincPy check (not always) that a winc/files/cache/cache folder
# was created, which then caused some of the errors.
#
# The function below, which is called inside the clean_cache() and cached_files()
# functions, ensures that the path always returns to ../Winc/files/ , after I
# implemented this the WincPy check passed everything.

def goto_files_folder_path():
    # Change working directory to the one that the
    # current 'main.py' script is operating from:
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)
    return


def clean_cache():
    # Ensure that path first goes to ../files/ folder, see comments above:
    goto_files_folder_path()
    entries = os.listdir()
    # Check for presence of 'cache' folder:
    if "cache" not in entries:
        # If not present yet, make one:
        os.mkdir('cache')
    else:
        # ...but if already present, first delete it,
        # including file contents and subdirectories:
        shutil.rmtree('cache')
        # ...and then create brand new 'cache' folder:
        os.mkdir('cache')
        
#         # Alternative solution (but more cumbersome),
#         # this also works and passes the WincPy check:
#         path = pathlib.Path.cwd() / 'cache'
#         os.chdir(path)
#         cache_entries = os.listdir()
#         for entry in cache_entries:
#             if os.path.isfile(entry):
#                 os.remove(entry)
#             elif os.path.isdir(entry):
#                 shutil.rmtree(entry)
    
    # Ensure that path returns to ../files/ folder:
    goto_files_folder_path()
    return


def cache_zip(zip_file_path, cache_dir_path):
    # This method will in fact create the folder cache_dir_path,
    # if it wasn't present yet.  So with this shutil method,
    # using the previous clean_cache() function might be no longer needed.
    shutil.unpack_archive(zip_file_path, cache_dir_path)
    return


def cached_files():
    # Check for presence of 'cache' folder in current directory:
    if "cache" in os.listdir():
        # Change directory to 'cache' folder:
        path = pathlib.Path.cwd() / 'cache'
        os.chdir(path)
    else:
        path = pathlib.Path.cwd()
        print("There is no 'cache' folder yet in current directory.")
    
    file_list = []
    for entry in os.scandir(path):
        # Check for each item in 'cache' folder whether it's a file
        # (i.e. excluding subfolders), and only append those
        # to the file_list as absolute path names, using the
        # .path method:
        if entry.is_file():
            file_list.append(entry.path)
    
    # Ensure that path returns to ../files/ folder:
    goto_files_folder_path()
    return file_list


def find_password(file_list):
    for file in file_list:
        # First read the entire text file
        # into a string variable, to easily check whether
        # the substring 'password' is present in it;
        # the 'with' statement ensures the file
        # is closed after it's read:
        with open(file, 'r') as fileObject:
            file_string = fileObject.read()
        
        # Now open the file again, and make
        # a list of each separate line (needed
        # below in case the file contains 'password').
        # As a sidenote, I discovered the .read() and .readlines()
        # methods cannot be used within the same
        # 'with' statement, if so the latter one that is used
        # doesn't actually open the file anymore.
        with open(file, 'r') as fileObject:
            list_of_lines = fileObject.readlines()
            
        if 'password' in file_string.lower():
            for line in list_of_lines:
                if 'password' in line.lower():
                    # Split up the line in the file
                    # that contains the 'password' string,
                    # into a list of words, using spaces
                    # as separators:
                    wordList = line.rsplit()
                    i = 0
                    for word in wordList:
                        # Assume that if the 'password'
                        # substring is found in one of the
                        # word strings, then the NEXT word
                        # item in the list (so with index i+1)
                        # will be the actual password:
                        if 'password' in word.lower():
                            password = wordList[i+1]
                        i += 1
    
    return password
