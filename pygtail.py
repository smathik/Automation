
from os import stat
from sys import exit
from sys import argv
from sys import getsizeof
from collections import defaultdict
from collections import deque
import fcntl
import os
import re
import pygtail
import getopt
import yaml
import csv

def get_yaml_config(config_file):
  with open(config_file) as yaml_config_data:
    pydata = yaml.load(yaml_config_data)
  return pydata

def pygtail_open(config_dict):
  pygtail_log = pygtail.Pygtail(config_dict['name'], offset_file=config_dict['offset_file'])
  return pygtail_log

def make_offset_dir(offset_file):
  parent_dir =  os.path.abspath(os.path.join(offset_file, os.pardir))
  if not os.path.isdir(parent_dir):
    try:
      os.makedirs(parent_dir, mode=0755)
    except:
      print 'unable to make directory ' + parent_dir
      exit(2)

def check_if_run_and_temp_file_exists(offset_file, inode_temp_file):
  if not os.path.exists(offset_file) | os.path.exists(inode_temp_file):
    file(offset_file, 'w').close()
    file(inode_temp_file, 'w').close()

def pygtail_chunk(pygtail_log, chunk_size_mb, pygtail_end):
  chunk_size_bytes=chunk_size_mb * 1024 * 1024
  pygtail_string=''
  while getsizeof(pygtail_string) < chunk_size_bytes:
    try:
      pygtail_string = pygtail_string + pygtail_log.next()
    except StopIteration:
      pygtail_end=True
      break
  return pygtail_string, pygtail_end

def regex_func(regex, pygtail_string):
  pygtail_string = re.findall("^.*%s.*$"%regex, pygtail_string, re.M | re.I)
  return  '\n'.join(map(str, pygtail_string))

def ignore_func(regex, pygtail_string):
  string = ""
  for itr in pygtail_string.split("\n"):
   if not re.findall("^.*%s.*$"%regex, itr, re.I):
     string += itr+"\n"
  return string[:-1]

def awk_func(field, pygtail_string):
  string = ""
  for itr in pygtail_string.split("\n"):
    try:
     string += itr.split()[field] + "\n"
    except IndexError:
     continue
  return string[:-1]

def log_regex_match(config_dict, pygtail_string):
  for match_string_def in config_dict['strings']:
   itr_string = pygtail_string
   for temp in match_string_def['processes']:
      if temp['process'] == "regex":
       itr_string = regex_func(temp['regex'], itr_string)
      elif temp['process'] == "ignore":
       itr_string = ignore_func(temp['regex'], itr_string)
      elif temp['process'] == "awk":
       itr_string = awk_func(temp['field'], itr_string)
   match_number = len(filter(None, itr_string.split("\n")))
   try:
      config_dict['string_matches'][match_string_def['name']] = config_dict['string_matches'][match_string_def['name']] + match_number
   except KeyError:
      config_dict['string_matches'][match_string_def['name']] = match_number
  return config_dict

def error_warn_stdout(config_data):
  config_data['exit_code'] = 0
  config_data['perf_data'] = ' |'
  config_data['success_msg'] = 'OK No Errors '
  config_data['critical_msg'] = 'Critical'
  config_data['warn_msg'] = 'Warning'
  d = defaultdict(list)
  for config_dict in config_data['logs']:
    try:
      if config_dict['isCsv'] == True:
        pass
    except KeyError:
      for match_string_def in config_dict['strings']:
        try:
          match_string_def['error']
        except KeyError:
          match_string_def['error'] = 0
        try:
          match_string_def['warn']
        except KeyError:
          match_string_def['warn'] = 0
        if config_dict['string_matches'][match_string_def['name']] >= match_string_def['error'] and match_string_def['error'] != 0:
          if config_data['exit_code'] <= 2:
            config_data['exit_code'] = 2
            d[config_data['critical_msg']].append( match_string_def['name']  + '(' + str(config_dict['string_matches'][match_string_def['name']]) +'gt' + str(match_string_def['error']) + '(' + config_dict['name'].split('/')[-1] + '))')
        elif config_dict['string_matches'][match_string_def['name']] >= match_string_def['warn'] and match_string_def['warn'] != 0:
          if config_data['exit_code'] <= 1:
            config_data['exit_code'] = 1
            d[config_data['warn_msg']].append( match_string_def['name'] + '(' + str(config_dict['string_matches'][match_string_def['name']]) +'gt' + str(match_string_def['warn']) + '(' + config_dict['name'].split('/')[-1] + '))')
        config_data['perf_data'] = config_data['perf_data'] + " \'" + match_string_def['name'] + "\'=" + str(config_dict['string_matches'][match_string_def['name']]) + ";" + str(match_string_def['warn']) + ";" + str(match_string_def['error'])
  config_data.update(dict(d))
  return config_data



def csv_operation(config_dict):
  csv_file = open(config_dict['name'], 'rb')
  reader = csv.reader(csv_file)
  headers = reader.next()
  lastrow = deque(csv.reader(csv_file), 1)[0]
  csv_output, csv_warn, csv_crit = "", "", ""
  csv_output += " '%s'=%s;0;0 "%(headers[0],lastrow[0])
  for i in config_dict['strings']:
   for head, row in zip(headers[1:], lastrow[1:]):
    head ,name , row= head.strip().lower(), i['name'].strip().lower(), row.strip()
    if row == "":
       row = int('0'+row)
    else:
       row = float(row)
    if head == name:
      if row > int(i['error']) and  int(i['error']) != 0:
        csv_crit += " %s(%dgt%d(%s)); "%(head,row,i['error'],config_dict['name'])
      elif row > int(i['warn']) and int(i['warn']) != 0:
        csv_warn += " %s(%dgt%d(%s)); "%(head, row,i['warn'],config_dict['name'])
      csv_output += " '%s'=%d;%d;%d "%(head,row,i['warn'],i['error'])

  return (csv_output, csv_warn, csv_crit)



def log_analyze(config_data):
  csv_outputs, csv_warn_output, csv_crit_output = "", "", ""
  for config_dict in config_data['logs']:
    try:
      if config_dict['isCsv'] == True:
        csv_output, csv_warn, csv_crit  = csv_operation(config_dict)
        csv_outputs += csv_output
        csv_warn_output += csv_warn
        csv_crit_output += csv_crit
    except KeyError:
      config_dict['string_matches'] = {}
      make_offset_dir(config_dict['offset_file'])
      check_if_run_and_temp_file_exists(config_dict['offset_file'],config_dict['inode_temp_file'])
      getPreviousRunLogInode(config_dict['name'],config_dict['offset_file'],config_dict['inode_temp_file'])
      pygtail_log = pygtail_open(config_dict)
      pygtail_end = False
      while pygtail_end is False:
        (pygtail_string, pygtail_end) = pygtail_chunk(pygtail_log, config_dict['chunk_size_mb'], pygtail_end)
        config_dict = log_regex_match(config_dict, pygtail_string)
  config_data = error_warn_stdout(config_data)
  try:
    try:
      try:
        print 'Critical : ' + '; '.join(map(str,config_data['Critical'])) + csv_crit_output + config_data['perf_data'] + csv_outputs
      except KeyError:
        if not csv_crit_output:
          raise KeyError
        print 'Critical : ' + csv_crit_output + config_data['perf_data'] + csv_outputs
    except KeyError:
      try:
        print 'Warning : ' + '; '.join(map(str,config_data['Warning'])) + csv_warn_output + config_data['perf_data'] + csv_outputs
      except KeyError:
        if not csv_warn_output:
          raise KeyError
        print 'Warning : ' + csv_warn_output + config_data['perf_data'] + csv_outputs
  except KeyError:
        print config_data['success_msg'] + config_data['perf_data'] + csv_outputs
  exit(config_data['exit_code'])

def getPreviousRunLogInode(name,offset,file_name):
  if not os.path.exists(file_name):
    open(file_name, 'w').close()
  if os.stat(file_name).st_size == 0:
    text_file = open(file_name, "wb")
    old_file_inode1 = 0
    text_file.write(str(old_file_inode1))
    text_file.close()
  text_file1 = open(file_name, "r")
  old_file_inode = text_file1.readlines()
  old_file_inode1 = int(old_file_inode[0])
  text_file1.close()
  text_file2 = open(file_name, "w+")
  text_file2.seek(0)
  text_file2.truncate()
  text_file2.close()
  newFileInode(name,file_name,old_file_inode1,offset)

def newFileInode(log_name,name,old_file_inode1,offset):
  new_file_inode = os.stat(log_name).st_ino
  text_file3 = open(name, "w+")
  text_file3.write(str(new_file_inode))
  text_file3.close()
  with open(offset, 'r') as f:
    try:
      lines_off = f.read().splitlines()
      offset_value = int(lines_off[-1])
    except IndexError:
      offset_value = 0
  log_char_count = 0
  if old_file_inode1 != new_file_inode:
    open_file = open(offset, "w+")
    open_file.seek(0)
    open_file.truncate()
    open_file.close()
  elif stat(log_name).st_size < offset_value:
    open_file = open(offset, "w+")
    open_file.seek(0)
    open_file.truncate()
    open_file.close()

def main(current_script, argv):
  pidfile = open('/var/tmp/log_analyze.pid', 'w')
  try:
    fcntl.lockf(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
  except IOError:
    print "Failed file lock other instances of log_analyze are running.\n Only run one instance at a time."
    exit(2)
  try:
    opts, args = getopt.getopt(argv, "hc:")
  except getopt.GetoptError:
    print current_script + ' -c <config_file>'
    exit(2)
  if len(opts) < 1:
    print current_script + ' -c <config_file>'
    exit(2)
  for opt, arg in opts:
    if opt not in("-c"):
      print current_script + ' -c <config_file>'
      exit(2)
    elif opt in("-c"):
      config_file = arg
  config_data = get_yaml_config(config_file)
  output_data = log_analyze(config_data)

if __name__ == '__main__':
  main(argv[0], argv[1 : ])
