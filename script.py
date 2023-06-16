import argparse
import json
import os
from typing import List
import tableauserverclient as TSC
from PyPDF2 import PdfMerger
from tableauserverclient import RequestOptions, Filter


class TableauPdfExporter:
    def __init__(self, server_url="company.tableau.com", server_version="3.11"):
        self.server_url = server_url
        self.server_version = server_version
        self.server = None

    def connect(self, token_name: str, token_value: str, site_name: str = "") -> None:
        """
        Establish a connection to the Tableau Server.

        Parameters:
        token_name (str): Name of the personal access token.
        token_value (str): Value of the personal access token.
        site_name (str, optional): Name of the site. Defaults to "".
        """
        tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_name)
        self.server = TSC.Server(self.server_url)
        self.server.add_http_options({"verify": False})
        self.server.version = self.server_version
        try:
            self.server.auth.sign_in(tableau_auth)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Tableau Server: {e}")

    def get_workbook(self, workbook_name: str, project_name: str) -> TSC.WorkbookItem:
        """
        Retrieve the workbook from the Tableau Server.

        Parameters:
        workbook_name (str): The name of the workbook.
        project_name (str): The name of the project.

        Returns:
            TSC.WorkbookItem: The workbook item.
        """
        req_option = RequestOptions()
        req_option.filter.add(
            Filter("name", TSC.RequestOptions.Operator.Equals, workbook_name)
        )

        workbooks = list(TSC.Pager(self.server.workbooks, req_option))

        workbook = [w for w in workbooks if w.project_name == project_name]

        if len(workbook) == 0:
            raise ValueError(
                f"Workbook {workbook_name} not found in project {project_name}"
            )

        workbook = workbook[0]

        # Populate the workbook with the views
        self.server.workbooks.populate_views(workbook)

        print(f"Found workbook {workbook.name} in project {workbook.project_name}")

        return workbook

    def get_workbook_view(
        self, workbook: TSC.WorkbookItem, view_name: str
    ) -> TSC.ViewItem:
        """
        Retrieve the specified view from the workbook.

        Parameters:
        workbook (TSC.WorkbookItem): The workbook item.
        view_name (str): The name of the view.

        Returns:
        TSC.ViewItem: The view item.
        """
        view = [v for v in workbook.views if v.name == view_name]

        if len(view) == 0:
            raise ValueError(f"View {view_name} not found in workbook {workbook.name}")

        view = view[0]

        print(f"Found view {view.name} in workbook {workbook.name}")

        return view

    def get_view_pdf_with_filter(self, filter: list, view_item: TSC.ViewItem) -> bytes:
        """
        Generate a PDF of the view with the specified filter.

        Parameters:
        filter (list): The filter to apply.
        view_item (TSC.ViewItem): The view item.

        Returns:
        bytes: The PDF file in bytes.
        """
        print(f"Generating PDF for view {view_item.name} with filter {filter}")
        pdf_req_option = TSC.PDFRequestOptions()
        if filter:
            for f in filter:
                filter_name, filter_value = f

                # Cheap Escaping fix for commas and ampersands
                # TODO: Make this better and handle when commas are needed for multiple values
                filter_value = filter_value.replace("&", "%26").replace(",", "%5C,")
                filter_name = filter_name.replace("&", "%26").replace(",", "%5C,")

                pdf_req_option.vf(filter_name, filter_value)
            self.server.views.populate_pdf(view_item, pdf_req_option)
        else:
            self.server.views.populate_pdf(view_item)

        return view_item.pdf

    @staticmethod
    def save_pdf_to_directory(
        pdf_file: bytes, file_name: str, directory: str = "output"
    ) -> str:
        """
        Save the PDF file to the specified directory.

        Parameters:
        pdf_file (bytes): TheI apologize for the premature termination of the previous message. Here is the continuation and completion of the refactored code:

        Returns:
        pdf_file (bytes): The PDF file in bytes.
        file_name (str): The name of the file.
        directory (str, optional): The directory to save the file. Defaults to "output".
        """
        os.makedirs(directory, exist_ok=True)

        output_file = f"{directory}/{file_name}.pdf"

        with open(output_file, "wb") as f:
            f.write(pdf_file)

        return output_file

    @staticmethod
    def merge_pdfs_from_directory(directory: str = "output") -> str:
        """
        Merge all PDFs in the specified directory into a single file.

        Parameters:
        directory (str, optional): The directory containing the PDF files. Defaults to "output".

        Returns:
        str: The path of the merged PDF file.
        """
        merger = PdfMerger()

        pdfs = [f for f in os.listdir(directory) if f.endswith(".pdf")]

        # Reverse so order so that the first page is the first PDF
        pdfs.sort(reverse=True, key=str.lower)

        for pdf in pdfs:
            print(f"Merging {pdf}")
            merger.append(f"{directory}/{pdf}")

        merged_file_path = f"{directory}/merged_pdfs.pdf"
        merger.write(merged_file_path)
        merger.close()

        # Remove individual PDF files after merging
        for pdf in pdfs:
            os.remove(f"{directory}/{pdf}")

        return merged_file_path

    @staticmethod
    def load_config(config_file: str = "config.json") -> List[dict]:
        """
        Load the configuration from the specified JSON file.

        Parameters:
        config_file (str, optional): The path of the configuration file. Defaults to "config.json".

        Returns:
        List[dict]: The configuration.
        """
        with open(config_file, "r") as f:
            return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Export a view as an image, PDF, or CSV"
    )
    parser.add_argument("--server", "-s", help="server address")
    parser.add_argument("--site", "-S", help="site name")
    parser.add_argument(
        "--token-name",
        "-p",
        help="name of the personal access token used to sign into the server",
    )
    parser.add_argument(
        "--token-value",
        "-v",
        help="value of the personal access token used to sign into the server",
    )
    parser.add_argument("--version", "-V", default="3.11", help="server version")

    args = parser.parse_args()

    exporter = TableauPdfExporter(server_url=args.server, server_version=args.version)
    exporter.connect(args.token_name, args.token_value, args.site)

    workbooks = exporter.load_config()
    for i, workbook in enumerate(workbooks):
        wb_name, wb_project, wb_view, wb_filters = workbook.values()
        wb = exporter.get_workbook(wb_name, wb_project)
        view = exporter.get_workbook_view(wb, wb_view)
        pdf_name = f"{i}_{workbook['name']}"
        pdf_file = exporter.get_view_pdf_with_filter(wb_filters, view)
        saved_pdf = exporter.save_pdf_to_directory(pdf_file, pdf_name)

    merged_pdf = exporter.merge_pdfs_from_directory("output")
    print(f"PDF file saved to {merged_pdf}")


if __name__ == "__main__":
    main()
