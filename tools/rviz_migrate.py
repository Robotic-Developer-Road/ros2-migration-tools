#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
Author: sujit-168 su2054552689@gmail.com
Date: 2025-02-09 16:30:58
FilePath: ros_migrate_tools/rviz_migrate.py
Description: a script to migrate rviz files from rviz to rviz2
'''

import argparse

def migrate_rviz_file(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        filedata = file.read()

    # Replace all rviz/ fields
    filedata = filedata.replace('rviz/', 'rviz_default_plugins/')

    # Replace the specific fields
    specific_fields = ['rviz_default_plugins/Displays',
                        'rviz_default_plugins/Help',
                        'rviz_default_plugins/Selection',
                        'rviz_default_plugins/Time',
                        'rviz_default_plugins/Tool Properties',
                        'rviz_default_plugins/Transformation',
                        'rviz_default_plugins/Views',
                        'rviz_default_plugins/Group',
                        ]
    for field in specific_fields:
        filedata = filedata.replace(field, field.replace('rviz_default_plugins/', 'rviz_common/'))

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Migrate RViz config file.')
    parser.add_argument('file_path', type=str, help='The absolute path to the .rviz file')
    args = parser.parse_args()

    migrate_rviz_file(args.file_path)
