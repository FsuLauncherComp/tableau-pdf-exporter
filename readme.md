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
    git clone https://github.com/FsuLauncherComp/tableau-pdf-exporter.git
    ```
2. Navigate to the project root:
    ```
    cd tableau-pdf-exporter
    ```
    
    2.1 (Optional) Create a virtual environment:
    ```
    python -m venv venv
    ```

    2.2 (Optional) Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
3. Install the required Python libraries:
    ```
    pip install -r requirements.txt
    ```
4. Update the 'config.json' file in the project root with your configurations. The file should be structured as follows (note the order determines the order of the exported PDFs in the merged file):
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
      server url address
  --site SITE, -S SITE
      site name
  --token-name TOKEN_NAME, -p TOKEN_NAME 
      name of the personal access token used to sign into the server
  --token-value TOKEN_VALUE, -v TOKEN_VALUE
      value of the personal access token used to sign into the server
  --version VERSION, -V VERSION
      server version
```
