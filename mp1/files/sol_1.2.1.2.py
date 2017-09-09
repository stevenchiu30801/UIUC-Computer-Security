import sys
from pymd5 import md5, padding
from urllib import quote
import re

query_file = sys.argv[1] 
command3_file = sys.argv[2] 
output_file = sys.argv[3]

with open(query_file) as f:
	query = f.read().strip()

with open(command3_file) as f:
	command3 = f.read().strip()

m = re.search(r'user=.*', query).group() # match user=...&commands
length_of_m = 8 + len(m) # 8 is password length
bits = (length_of_m + len(padding(length_of_m * 8))) * 8
token = re.search(r'(?<=token=)[0-9a-fA-F]+(?<!&)', query).group() # match the token

h = md5(state = token.decode('hex'), count = bits)
h.update(command3)
new_token = h.hexdigest()

with open(output_file, 'w') as f:
	f.write("token=" + new_token + "&" + m + quote(padding(length_of_m * 8)) + command3)