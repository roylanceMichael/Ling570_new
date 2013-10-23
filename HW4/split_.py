import re
import sys

def main():

  l = sys.stdin.read()
  for ch in l:
    l = re.sub(ch, ch+' ', l)
  l = re.sub('\s{2,}', ' ', l)
  print l



if __name__ == '__main__':
  main()

