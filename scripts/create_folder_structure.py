import argparse

parser = argparse.ArgumentParser(
                    prog='Research Record Folder Structure Setup',
                    description='\n'.join([
                        'Python script to set up a new research record folder.',
                        ''
                    ]))
parser.add_argument('name', help='Name of the folder to create')
parser.add_argument('--structure', default='default', help='File containing a JSON file of the structure.\nWhere folders are named lists and files are names within a list.\nWarning, JSON is always in-place.\nInbuilt structures: default, QC')
parser.add_argument('--inplace', '-i', default=False, action=argparse.BooleanOptionalAction, help='Creates the folder structure in current directory, equivalent of using name="."')
parser.add_argument('--eg', default=None, choices=['default', 'QC'], help='Print the example JSON structure of the folder')
parser = parser.parse_args()

print('Running script with the following arguments')
print(parser)

import os
import json
from pathlib import Path

default_structure = {
    parser.name:[
        'about.md',
        'literature.md',
        'meetings.md',
        {'data':[
            {'raw':[]},
            {'processed':[]},
            {'intermediate':[]}]},
        {'code': []},
        {'results':[
            {'raw':[]},
            {'figures':[]},
            {'tables':[]}]},
        {'exploratory': []}
]}

QC_structure = {
    parser.name:[
        'about.md',
        'literature.md',
        'meetings.md',
        {'data':[]},
        {'reports':[]}
    ]
}

inbuilt_structures = {'default': default_structure,
                     'QC': QC_structure}

if parser.eg is not None:
    print(json.dumps(inbuilt_structures[parser.eg]))
    quit()
if parser.structure is not None:
    if parser.structure in inbuilt_structures.keys():
        structure = inbuilt_structures[parser.structure]
    else:
        with open(parser.structure, 'r') as f:
            structure = json.load(f)
else:
    structure = default_structure
if parser.inplace:
    structure['.'] = structure.pop(parser.name)

def walk_path(base, structure):
    paths = []
    # Return the file structure if it's a file
    if isinstance(structure, str):
        paths.append(os.path.join(base, structure))
    # If it's a list, repeat 'walk_path' for each item
    elif isinstance(structure, list):
        if len(structure)==0:
            structure = ['']
        for val in structure:
            new_paths = walk_path(base, val)
            paths.extend(new_paths)
    # If it's a dictionary, we need to extend the folder path
    # We repeat 'walk_path' using the key
    elif isinstance(structure, dict):
        for key, val in structure.items():
            new_paths = walk_path(key, val)
            paths.append(os.path.join(base, key, ''))
            paths.extend([os.path.join(base, x) for x in new_paths])
    return paths
    
files_to_create = walk_path('.', structure)
for file in files_to_create:
    if file.endswith('/') or file.endswith('\\'):
        Path(file).mkdir(exist_ok=True)
    else:
        Path(file).touch()
