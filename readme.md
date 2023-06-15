# Tableau PDF Exporter

This Python-based tool uses the Tableau Server Client library to export views from Tableau Workbooks as PDF files. It allows the user to specify filters to apply to the views before exporting. Moreover, it provides the capability to merge all exported PDFs into a single file.

## Features
1. Connects to a Tableau Server using a personal access token.
2. Retrieves a specified workbook(s) from the server.
3. Exports a specified view(s) from the workbook as a PDF file.
4. Allows applying filters to the views before exporting.
5. Saves the exported PDF files to a specific directory.
6. Merges all the exported PDFs in a directory into one file.

## Requirements
- Python 3.6 or newer.
- 'tableauserverclient' Python library.
- 'PyPDF2' Python library.

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/your-repo/tableau-pdf-exporter.git
    ```
2. Enter the repository directory:
    ```
    cd tableau-pdf-exporter
    ```
3. Install the required Python libraries:
    ```
    pip install -r requirements.txt
    ```
4. Create a 'config.json' file in the project root with your configuration. The file should be structured as follows:
```json
    [
        {
            "name": "workbook_name",
            "project": "project_name",
            "view": "view_name",
            "filters": [
                ["filter_name", "filter_value"]
            ]
        }
    ]
```

## Usage
```
usage: main.py [-h] [--server SERVER] [--site SITE] [--token-name TOKEN_NAME] [--token-value TOKEN_VALUE]  [--version VERSION]

Export multiple dashboards as PDF, apply filters to the dashboards before exporting, and merge all the exported PDFs into one file.

optional arguments:
  -h, --help 
    show this help message and exit
  --server SERVER, -s SERVER 
    server address
  --site SITE, -S SITE
    site name
  --token-name TOKEN_NAME, -p TOKEN_NAME 
    name of the personal access token used to sign into the server
  --token-value TOKEN_VALUE, -v TOKEN_VALUE
    value of the personal access token used to sign into the server
  --version VERSION, -V VERSION
    server version
```
