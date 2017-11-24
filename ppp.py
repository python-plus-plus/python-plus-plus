import os.path
import re
import subprocess
import sys


ppp_lib_imports = "import ppp_lib\n"

def strip_comments(s):
    return re.sub(r"^[\t ]*\#.*$", '', s, flags=re.MULTILINE)

def increment(str, in_func):
    return re.sub(r"(\w+)\+\+", r"ppp_lib.incdec.PostIncrement('\1', locals())", str)

def mutable_args(func_def):
    pass

def deep_copy(str):
    pass

def tail_call(func_def):
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('invalid args')
        sys.exit(-1)

    input_file_path = os.path.abspath(sys.argv[1])

    if (not os.path.isfile(input_file_path)):
        print('invalid file')
        sys.exit(-1)

    input_file_basename = os.path.basename(input_file_path)
    filename, input_file_ext = os.path.splitext(input_file_basename)
    if (input_file_ext != '.ppp'):
        print('input file not a Python++ file.')
        sys.exit(-1)

    compiled_file_path = os.path.join(os.path.dirname(input_file_path), filename + '.py')

    fin = open(input_file_path, 'r')
    fout = open(compiled_file_path, 'w')


    ppp_source = ''.join(fin.readlines())
    fin.close()


    # start transforms
    ppp_source = strip_comments(ppp_source)
    # TODO: fix in/out of function detection
    ppp_source = increment(ppp_source, False)

    # TODO: string removal/reinsertion


    fout.write(ppp_lib_imports)
    fout.write(ppp_source)
    fout.close()

    # start regular python interpreter and exit
    # TODO: uncomment
    # subprocess.Popen(['python', compiled_file_path])
    # sys.exit(0)