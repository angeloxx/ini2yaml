import argparse, os, sys, configparser, yaml
from itertools import chain

configContent=dict()

def main():
  parser = argparse.ArgumentParser(description="Convert ini to Yaml")
  parser.add_argument('--path', metavar='path', default=".", help="Input path or file")
  parser.add_argument('--out', metavar='out', default="out.yaml", help="Input path or file")
  args = parser.parse_args()

  if os.path.isdir(args.path):
    for filename in os.scandir(args.path):
      if filename.is_file() and filename.path != args.out:
        readIniFile(filename.path)
  elif os.path.isfile(args.path):
      readIniFile(args.path)
  else:
      print(f"File or path {args.path} does not exist")
  
  with open(args.out, 'w') as file:
    yaml.dump(configContent, file)


def readIniFile(file):
  try:
    config = configparser.ConfigParser()
    with open(file) as lines:
        lines = chain(("[top]",), lines)
        config.read_file(lines)
    print(f"File {file} read with success")
  except:
    print(f"File {file} skipped, contains errors")
  
  for key,value in config.items("top"):
    parent = configContent
    for subkey in key.split("."):
      if key.split(".").index(subkey) == len(key.split("."))-1:
        parent[subkey] = value
      else:
        if not subkey in parent:
          parent[subkey] = dict()
        parent = parent[subkey]

if __name__ == '__main__':
  sys.exit(main())  # next section explains the use of sys.exit
