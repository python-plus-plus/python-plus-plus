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
    if len(function_starts) > len(function_ends) and len(code_lines[line]) > 0 \
       and code_lines[line][0] != ' ':
      function_ends.append(line) 

    # Look for a function start.
    if code_lines[line].startswith('def '):
      function_starts.append(line)

    line += 1

  if len(function_starts) > len(function_ends):
    function_ends.append(line)

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
  """
  Given a function definition, identify all tail self-recursive calls and
  handle them accordingly.
  """
  # Identify the indent amount
  first_indented_line = [e for e in func_def.split("\n") if len(e) > 0 and e[0] == ' '][0]
  indent = re.match(r"^([\t ]*)", first_indented_line).group(1)

  # Identify the function name
  header_pattern = r"def[\t ]*(?P<name>[A-Za-z_]\w*)\(.*\):\n"
  header = re.search(header_pattern, func_def)
  func_name = header.group("name")

  # Find (for now only single line) recursive calls. Store their line number iff 
  # it appears to be a tail recursive call.
  code_lines = func_def.split("\n")
  line = 0
  tail_calls = []
  while line < len(code_lines):
    stripped_line = code_lines[line].strip()    
    line += 1

    # Continue if it doesn't start with a return 
    if not (stripped_line.startswith("return %s" % func_name) or
            stripped_line.startswith(func_name)):
      continue

    # Continue if the line ends in something other than a close paren.
    # Obviously, this is not robust, but we assume it's sufficient.
    if not stripped_line.endswith(")"):
      continue

    # If we've made it this far, add the line number (of cur iteration).
    tail_calls.append(line-1)
   
  # Parse out the parameters (assume no keyword arguments)
  param_pattern = r"def[\t ]*[A-Za-z_]\w*\((?P<args>.*)\):\n"
  parameters = re.search(param_pattern, func_def).group('args')
  # Now process all of the tail calls.    
  for i in tail_calls:
    # Retrieve the tail recursive call
    tail_call_line = code_lines[i]
 
    # Parse out the arguments. Assume no nested brackets, simple functional
    # call.
    start_index = tail_call_line.index("(")
    end_index = tail_call_line.index(")")
    args = tail_call_line[start_index+1:end_index]

    # Get indent of the tail call line
    tail_indent = re.match(r"^([\t ]*)", tail_call_line).group(1)

    # Create two lines: 1. updating params, 2. raising a StopIteration error
    update_line = tail_indent + parameters + " = " + args + "\n"
    error_line = tail_indent + "raise ppp_lib.tail_call.NextCall"

    # Replace the tail call line with the modified version
    func_def = func_def.replace(tail_call_line, update_line + error_line)     
    
  # Indent all of the function definition (after the header on the first line)
  code_lines = func_def.split("\n")

  # Indent every line after the header
  code_lines = [2*indent+line if i > 0 else line for i,line in enumerate(code_lines)]
 
  # Insert a while True as the first line after the header 
  code_lines.insert(1, indent + "while True:")

  # Insert a try statement as the second line after the header
  code_lines.insert(2, indent*2 + "try:")

  # Insert a break right after the code. If we've made it this far without a function call,
  # we would usually exit out without a return statement. Since we don't want to infinite loop
  # we have to do this by breaking out of the while True loop.
  code_lines.append(3*indent + "break")

  # The very last lines will be catching the exception and continuing the outer loop.
  code_lines.append(2*indent + "except ppp_lib.tail_call.NextCall:")
  code_lines.append(3*indent + "continue")

  return "\n".join(code_lines)

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
