import sys
import os


# input folder with xmls

if not sys.argv[1]:
   print (" Specify input folder with construct's xml files")

if not os.path.exists(sys.argv[1]):
   print (" Path doesn't exist")

INPUT_FOLDER = sys.argv[1]

# output folder to save xml
# just use where script runs
OUTPUT_FILE = os.path.join(os.getcwd(),"construct-es.xml")

# this is for better comparisson in diff tools-debuging
xml_order = ("common", "ui", "project", "undo", "alerts", "exporters", "plugins", "behaviors")

def content_file(path):
    with open(path,encoding="utf-8") as tmp:
         return tmp.read()

print (" getting files")

list_files = dict()
for root, subFolders, files in os.walk(INPUT_FOLDER):

    for filename in files:
        if filename == "leeme.txt":
           continue
        file_path = os.path.join(root,filename)

        current_filecontent = ""
        node_name = ""

        if "-" in filename:
           node_name = filename.split("-")[0]
           if not node_name in list_files:
              list_files[node_name] = dict()
              list_files[node_name]['children'] = list()

           list_files[node_name]['children'].append(file_path)
        else:
            list_files[filename.replace(".xml","")] = file_path


print (" merging files")
FINAL_FILE = ""
#join everything

for node_name in xml_order:
    content = list_files[node_name]
    if 'children' in content:
       tmp_content = ''

       for nody in content['children']:
           tmp_content += "\n" + content_file(nody)
       FINAL_FILE += "\n" + '<group name="' + node_name + '">' + tmp_content + '</group>'

    else:
         FINAL_FILE += "\n" + content_file(content)

FINAL_FILE = '﻿<?xml version="1.0" encoding="utf-8"?>\n<language name="English (US)" ietf-tag="en-US">\n' + FINAL_FILE  +'</language>'

with open(OUTPUT_FILE,"w",encoding="utf-8") as tmp:
     tmp.write(FINAL_FILE)

print (" done!")
