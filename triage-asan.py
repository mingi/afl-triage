import os
import sys
import subprocess
from shutil import copyfile


crashdir = ''
outdir = ''
binpath = ''

os.environ["ASAN_SYMBOLIZER_PATH"] = "/usr/lib/llvm-3.8/bin/llvm-symbolizer"

def execute(cmd) :
    fd = subprocess.Popen(cmd, shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    return fd.stdout, fd.stderr


binpath= sys.argv[1]
opt1 = sys.argv[2]
opt2 = sys.argv[3]
crashdir = sys.argv[4]
outdir = sys.argv[5]

print 'crashdir: ' + crashdir
print 'outdir: ' + outdir


crashes = os.listdir(crashdir)

crashes.sort()

bugs = []

call_stack = []

stack_depth = -1

is_call_stack = False

for filename in crashes:
#	full_filename = os.path.join(indir, filename)
# print (filename)
  
  if os.path.isdir(crashdir + filename) == True:
    continue

  cmd = binpath + " " + opt1 + " " + crashdir + '/' + filename + " " + opt2

  std_out, std_err = execute(cmd)
    
  is_segfault = False
    
  print filename

  lines = std_err.readlines()

  for line in lines:
    print line,

    if line.find("LargeMmapAllocator") >= 0:
      if not os.path.exists(outdir+'/LargeMmapAllocator'):
        os.makedirs(outdir+'/LargeMmapAllocator')
            
      copyfile(crashdir+'/'+filename, outdir+'/LargeMmapAllocator/'+filename)

      break

    if line.find("ERROR: AddressSanitizer") >= 0:
      is_call_stack = True

    if is_call_stack == True:
      stack_depth += 1
      if stack_depth > 1:
        print line,
        print stack_depth
        src_name = line.strip().split(' ')[4]
        file_name = src_name.split('/')[-1]

        print src_name
        print file_name

        call_stack.append(file_name)

        if stack_depth >= 4:
          is_call_stack = False
          stack_depth = -1

    if line.find("SUMMARY") >= 0:
      src_name = line.split(' ')[3]
      bug_name = src_name.split('/')[-1]
      bug_name = call_stack[0]+'_'+call_stack[1]+'_'+call_stack[2]

      if (bug_name in bugs) == False:
        print bug_name
        bugs.append(bug_name)

      if not os.path.exists(outdir+'/'+bug_name):
        os.makedirs(outdir+'/'+bug_name)
      
      print call_stack

      copyfile(crashdir+'/'+filename, outdir+'/'+bug_name+'/'+filename)

      call_stack = []
      break

    '''
    if line == lines[-1]:
      print line
      print 'no summary'

      if not os.path.exists(outdir+'/etc/'):
        os.makedirs(outdir+'/etc/')
      
      copyfile(crashdir+'/'+filename, outdir+'/etc/'+filename)
    '''

print 'count: ' + str(len(bugs))
    
