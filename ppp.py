import os.path
import re
import string
import subprocess
import sys

# welcome to that part of the source where random info is placed
#
# valid identifier regex (for Python 2.x, Python 3+ adds unicode
# which is way more complicated probably)
# [A-Za-z_]\w*


# TODO: make ppp_lib globally available as an installable package
ppp_lib_imports = "import ppp_lib\n"

def strip_comments(s):
  return re.sub(r"^[\t ]*\#.*$", '', s, flags=re.MULTILINE)


def increment(str):
  dec_replaced = re.sub(
    r"([A-Za-z_]\w*)\-\-",
    r"ppp_lib.incdec.PostDecrement('\1', locals(), globals())",
    str)
  inc_replaced = re.sub(
    r"([A-Za-z_]\w*)\+\+",
    r"ppp_lib.incdec.PostIncrement('\1', locals(), globals())",
    dec_replaced)
  return inc_replaced


def function_map(code_body, mod_func):
  """
  Given the entire code body, it identifies all instances of functions and
  processes them using the mod_func function.

  1. Identify all definitions of functions (not nested, not class methods).
  2. Call the mod_func function with the header/body of the function.
  3. Insert in the result.
  """
  # Given the limited scope of functions that we're handling, to find 
  # functions, we just need to find instances of the string 'def '

  # code_lines[function_starts[i] : function_ends[i]] should give us a 
  # function definition
  function_starts = []
  function_ends = []
  code_lines = code_body.split("\n")
  line = 0
  while line < len(code_lines):
    # If we haven't found the end for the function yet, look for the end.
    if len(function_starts) > len(function_ends) and not code_lines[line].startswith(' '):
      function_ends.append(line) 

    # Look for a function start.
    if code_lines[line].startswith('def '):
      function_starts.append(line)

    line += 1

  # Iterate over the identified function, modify the functions and replace 
  # them in the body.
  for start,end in zip(function_starts, function_ends):
    func_def = '\n'.join(code_lines[start:end])
    mod_func_def = mod_func(func_def)
    code_body = code_body.replace(func_def, mod_func_def)

  return code_body

def mutable_args_func(func_def):
  # TODO: make this code not shit and redundant
  header_pattern = r"def[\t ]*[A-Za-z_]\w*\((?P<args>.*)\):\n"
  header = re.search(header_pattern, func_def)
  arg_string = header.group('args')
  args = arg_string.split(',')
  args = [s.strip() for s in args if len(s.strip()) > 0]

  new_args = []
  for arg in args:
    arg_parts = [s.strip() for s in arg.split('=')]
    if len(arg_parts) == 2:
      arg_name = arg_parts[0]
      arg_default_val = arg_parts[1]

      mutable_arg_pattern = r"\[.*\]|\{.*\}"
      match = re.match(mutable_arg_pattern, arg_default_val)

      if (match):
        arg_val = re.sub(
          r"\[.*\]|\{.*\}",
          'ppp_lib.mutableargs.PPP_Sentinel_Obj(\'{0}\')'.format(arg_name),
          arg_default_val)
        new_args.append('{0}={1}'.format(arg_name, arg_val))
      else:
        new_args.append('{0}={1}'.format(arg_name, arg_default_val))
    else:
      new_args.append(arg_parts[0])

  # print(new_args)
  modified_header = header.group(0).replace(arg_string, ', '.join(new_args))

  # add checks to body
  func_body = re.sub(header_pattern, '', func_def)
  arg_checks = []
  for arg in args:
    arg_parts = [s.strip() for s in arg.split('=')]
    if len(arg_parts) == 2:
      arg_name = arg_parts[0]
      arg_default_val = arg_parts[1]

      mutable_arg_pattern = r"\[.*\]|\{.*\}"
      match = re.match(mutable_arg_pattern, arg_default_val)

      if match:
        first_indented_line = [e for e in func_body.split("\n") if len(e) > 0 and e[0] == ' '][0]
        indent = re.match(r"^([\t ]*)", first_indented_line).group(1)
        arg_check =  "{0}if (type({1}) is ppp_lib.mutableargs.PPP_Sentinel_Obj):\n"
        arg_check += "{0}    {1} = {2}"
        arg_check = arg_check.format(indent, arg_name, arg_default_val)
        arg_checks.append(arg_check)

  func_body = '\n'.join(arg_checks) + '\n' + func_body
  return modified_header + func_body


def deep_copy(str):
  mult_pattern = r"\][\t ]*\*[\t ]*([a-zA-Z0-9_-]+)"
  return re.sub(mult_pattern, r" for _ in range(\1)]", str)


def tail_call(func_def):
  return func_def

if __name__ == '__main__':
  # TODO: handle additional command line args to .py file
  if len(sys.argv) != 2:
    print('invalid args')
    sys.exit(-1)

  input_file_path = os.path.abspath(sys.argv[1])

  # do some basic sanity checks
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

  # TODO: some sort of chunk detection
  # then iterate over eg. def chunks and pass off to replacement functions
  ppp_source = deep_copy(ppp_source)
  ppp_source = function_map(ppp_source, mutable_args_func)
  ppp_source = function_map(ppp_source, tail_call)
  ppp_source = increment(ppp_source)

  # TODO: string removal/reinsertion

  fout.write(ppp_lib_imports)
  fout.write(ppp_source)
  fout.close()

  # start regular python interpreter and exit
  # TODO: uncomment to actually run the file
  subprocess.call('python3 %s' % compiled_file_path, shell=True)
  sys.exit(0)
