from services.managers.record_manager import RecordManager
from services.managers.sheet_manager import SheetManager
from services.managers.file_manager import FileManager
from services.data_relator import DataRelator
from services.api_service import ApiService


class MessageProcessor:
    """
    Main orchestrator for the data processing pipeline.
    Coordinates different stages without implementing business logic.
    """

    def __init__(self, data):
        self.data = data

        self.api = ApiService()
        self.buffers = {}
        self.result = {}
        self.sheets = {}

        self.file_manager = FileManager(self.data, self.buffers, self.api)
        self.record_manager = RecordManager(self.api, self.sheets)
        self.sheet_manager = SheetManager(self.buffers)
        self.data_relator = DataRelator(self.api)

    def process_data(self):
        """Main data processing pipeline."""
        self._process_and_upload_files()
        self._process_spreadsheets()
        self._create_and_relate_records()

    def _process_and_upload_files(self):
        """Process local files and upload only non-duplicated ones."""
        self.file_manager.process_and_upload()

    def _process_spreadsheets(self):
        """Process data from spreadsheets."""
        self.sheets.update(self.sheet_manager.process())

    def _create_and_relate_records(self):
        """Create records and establish relationships between entities."""
        self.record_manager.create_nfes()
        self.record_manager.create_sales()

        """Relate collections"""
        self.data_relator.relate_files_with_nfes()
        self.data_relator.relate_nfes_and_products_with_sales()