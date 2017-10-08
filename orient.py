import os
import sys
import subprocess
from shutil import copyfile


crash_files = []
queue_files = []

aflout = sys.argv[1]
outdir = sys.argv[2]


def find_parent(src, crash_dir):

  if src == '000000':
    return
    
  for filename in queue_files[1:]:
    if filename[3:9] == src:
      print filename
            
      start = filename.find('src:')

      copyfile(aflout+'/queue/'+filename, crash_dir+'/'+filename)

      find_parent(filename[start+4:start+10], crash_dir)
    
      break
	


print 'aflout: ' + aflout
print 'outdir: ' + outdir

crash_files = os.listdir(aflout+'/crashes/')
queue_files = os.listdir(aflout+'/queue/')

crash_files.sort()
queue_files.sort()


bug_ids = [];

for filename in crash_files[1:]:
  crash_dir = outdir + '/' + filename[3:9]

  if not os.path.exists(crash_dir):
    os.makedirs(crash_dir)

  copyfile(aflout+'/crashes/'+filename, crash_dir+'/'+filename)

  src_start = filename.find('src:')

  src = filename[src_start+4:src_start+10]

  find_parent(src, crash_dir)


