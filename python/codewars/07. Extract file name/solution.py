import re
class FileNameExtractor:
 def extract_file_name(dirty_file_name):
   return re.search('^\d+_(.*)\..*$', dirty_file_name).group(1)