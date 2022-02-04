#!/usr/bin/python
import argparse
import os
import sys

help_msg = "Provide an existing folder path"
parser = argparse.ArgumentParser(description="Generate index files recursively")
parser.add_argument('path', help=help_msg, type=str)

args = parser.parse_args()
print(args.path)
if os.path.exists(args.path) is False:
  print(help_msg)
  sys.exit(-1)


def process(path):
  filesAndDirs = os.listdir(path)
  if len(filesAndDirs)==0:
    print("Directory is empty. Moving on")
    return
  #has_index = bool([fod for fod in filesAndDirs if "index.ts" in fod])
  #if has_index:
  #  print("Index already created")
  #  return

  filesToExport = list(filter(lambda fod: "spec" not in fod and "index" not in fod and ".ts" in fod, filesAndDirs))
  dirs = list(filter(lambda fod: os.path.isdir(f"{path}/{fod}"), filesAndDirs))

  for d in dirs:
    # Look Ahead
    dPath = f"{path}/{d}"
    dFilesAndDirs = os.listdir(dPath) 
    if len(dFilesAndDirs)>0:
      process(dPath)
      if len(list(filter(lambda fod: ".ts" in fod, dFilesAndDirs))) > 0:
        filesToExport.append(d)

  export_lines = list(map(lambda file: f"export * from './{file.replace('.ts','')}'", filesToExport))

  f = open(f"{path}/index.ts", "w")
  f.writelines(f"{line};\n" for line in export_lines)
  f.close()

  

process(args.path)