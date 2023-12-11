import argparse
import xdg
import os
import requests

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
    template_directory = os.path.join(xdg.XDG_CONFIG_HOME, "template/templates")
    try:
        os.makedirs(template_directory)
    except OSError:
        return None
    print("Created config folder at " + str(xdg.XDG_CONFIG_HOME))
    downloadTemplates(template_directory)
    
def listTemplates():
    template_directory = os.path.join(xdg.XDG_CONFIG_HOME, "template/templates")
    for filename in os.listdir(template_directory):
        print(os.path.splitext(filename)[0])

parser = argparse.ArgumentParser(description='Creates templates for various programming languages and projects.')
parser.add_argument("input", metavar="type", nargs="?", help='Type of the template')
parser.add_argument("input", metavar="name", nargs="?", help='Name of the template')
parser.add_argument("-l", "--list", action="store_true", default=False, help="Lists the different templates available.")
args = parser.parse_args()

initConfig()
if args.list:
    listTemplates()
elif not args.input:
    print("A type and name are expected.")
else:
    print("Other stuff")

