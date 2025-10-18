from services.sheet_service import SheetService


class SheetManager:
    """Responsible for processing spreadsheets."""

    def __init__(self, buffers):
        self.buffers = buffers

    def process(self):
        """
        Process spreadsheet data.

        Returns:
            Dictionary with processed sales and nfes data
        """
        sheet_service = SheetService(self.buffers)
        return sheet_service.execute()
