
"""
Compile haml, coffeescript and sass files from a source directory to an
output directory.

$ pip install hamlpy
$ pip install CoffeeScript
$ pip install scss

"""

import os
import shutil
import coffeescript
from scss import parser
from hamlpy.hamlpy import Compiler

directory = os.path.dirname(os.path.abspath(__file__))
web_source_dir = os.path.join(directory, 'web_source')
web_build_dir = os.path.join(directory, 'web_build')


def work(input_file, func, output_file):
    print 'Compiling %s -> %s using %s.%s(..)' % (
        input_file,
        output_file,
        func.__module__,
        func.__name__
    )
    with open(input_file, 'r') as i:
        input_content = i.read()
    output_content = func(input_content)
    with open(output_file, 'w') as o:
        o.write(output_content)


def clean_directory(path):
    print 'Clearing "%s" ..' % path
    for f in os.listdir(path):
        sub_path = os.path.join(path, f)
        if f[0] != '.':
            if not os.path.isdir(sub_path):
                os.unlink(sub_path)
            else:
                clean_directory(sub_path)
        else:
            print 'Skipping %s' % sub_path


def clean_web_build():
    if os.path.exists(web_build_dir):
        print 'Cleaning Build Directory "%s" ..' % web_build_dir
        clean_directory(web_build_dir)
    else:
        print 'Creating Build Directory "%s" ..' % web_build_dir
        os.makedirs(web_build_dir)
    print 'Done'


def compile_files(subdir, ext, func):
    subdir_in_path = os.path.join(web_source_dir, subdir)
    subdir_out_path = os.path.join(web_build_dir, subdir)

    if os.path.isdir(subdir_in_path):
        if not os.path.isdir(subdir_out_path):
            os.makedirs(subdir_out_path)

        for f in os.listdir(subdir_in_path):
            if f[(-len(ext)):].lower() == ext.lower():
                file_in_path = os.path.join(subdir_in_path, f)
                file_out_path = os.path.join(subdir_out_path, f[:(-len(ext))])
                work(file_in_path, func, file_out_path)

def copy_files(subdir, ext=None):
    subdir_in_path = os.path.join(web_source_dir, subdir)
    subdir_out_path = os.path.join(web_build_dir, subdir)

    if os.path.isdir(subdir_in_path):
        if not os.path.isdir(subdir_out_path):
            os.makedirs(subdir_out_path)

        for f in os.listdir(subdir_in_path):
            if ext is None or f[(-len(ext)):].lower() == ext.lower():
                file_in_path = os.path.join(subdir_in_path, f)
                file_out_path = os.path.join(subdir_out_path, f)

                print 'Copying %s -> %s' % (file_in_path, file_out_path)
                shutil.copy2(file_in_path, file_out_path)


def main():
    haml_compiler = Compiler()

    clean_web_build()
    compile_files('', '.haml', haml_compiler.process)
    copy_files('javascripts', '.js')
    compile_files('javascripts', '.coffee', coffeescript.compile)
    copy_files('stylesheets', '.css')
    compile_files('stylesheets', '.scss', parser.parse)
    copy_files('images')


if __name__ == '__main__':
    main()
