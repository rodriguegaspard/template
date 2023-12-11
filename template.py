import argparse
import os
import re
import requests

# Template directory. Use whatever you like.
TEMPLATE_DIRECTORY = "/home/rosco/files/templates" 

def downloadTemplates(directory):
    # GitHub info
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    params = (
        ('ref', 'main'),
    )
    url = 'https://api.github.com/repos/rodriguegaspard/template/contents/templates'
    response = requests.get(url, headers=headers, params=params)
    downloaded_files = 0
    if response.status_code == 200:
    # Loop through each file and download it
        for file_info in response.json():
            file_url = file_info['download_url']
            file_name = file_info['name']
            file_response = requests.get(file_url, headers=headers)
            if file_response.status_code == 200:
                with open(os.path.join(directory, file_name), 'wb') as file:
                    file.write(file_response.content)
                    downloaded_files += 1
            else:
                print(f"Failed to download {file_name}")
        print("Downloaded " + str(downloaded_files) + " templates.")
    else:
        print("Failed to retrieve templates from GitHub API")

def initConfig():
    try:
        os.makedirs(TEMPLATE_DIRECTORY)
    except OSError:
        return None
    print("Created config folder at " + TEMPLATE_DIRECTORY)
    downloadTemplates(TEMPLATE_DIRECTORY)
    
def listTemplates():
    result_string = ""
    for filename in os.listdir(TEMPLATE_DIRECTORY):
        result_string += "\n" + os.path.splitext(filename)[0]
    return result_string

def createTemplate(type, name):
    pattern = ".*" + type + ".*"
    match_list = []
    for filename in os.listdir(TEMPLATE_DIRECTORY):
        if re.match(pattern, filename):
            match_list.append(filename)
    if len(match_list) == 0:
        print("No matches found for the template type. Here's the list of available templates.")
        print(listTemplates())
    elif len(match_list) > 1:
        print("Type is ambiguous. Please select the desired template.")
        for type in match_list:
            print(type)
    else:
        file_extension = os.path.splitext(match_list[0])[1]
        new_file = name + file_extension
        with open(os.path.join(os.fspath(TEMPLATE_DIRECTORY), match_list[0]), 'rb') as source:
            with open(new_file, 'wb') as destination:
                destination.write(source.read())

parser = argparse.ArgumentParser(description='Creates templates for various programming languages and projects.')
parser.add_argument("type", metavar="type", nargs="?", help='Type of the template')
parser.add_argument("name", metavar="name", nargs="?", help='Name of the template')
parser.add_argument("-l", "--list", action="store_true", default=False, help="Lists the different templates available.")
parser.add_argument("-d", "--download", action="store_true", default=False, help="Download the templates from GitHub.")
args = parser.parse_args()

initConfig()
if args.list:
    print(listTemplates())
if args.download:
    downloadTemplates(TEMPLATE_DIRECTORY)
elif not args.type or not args.name:
    print("A type and name are expected.")
else:
    createTemplate(args.type, args.name)
