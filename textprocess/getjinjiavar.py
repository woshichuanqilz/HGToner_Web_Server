# -*- coding: utf-8 -*-
import pandas as pd
import pypinyin
import datetime
import numpy as np
import sys
import re
import os
import time
from fuzzyfinder import fuzzyfinder

# Set Directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) # change to the path that you already know

with open('GetJinjaVariable.txt', encoding = 'utf-8') as the_file:
   content = the_file.read()

res_list = re.findall(r'(?<=\{\{).*(?=\}\})', content)
print(res_list)
