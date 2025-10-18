from services.file_service import FileService


class FileManager:
    """Responsible for processing and uploading files."""

    def __init__(self, data, buffers, api):
        self.buffers = buffers
        self.data = data
        self.api = api

    def process_and_upload(self):
        """
        Process local files and upload only non-duplicated ones.

        Returns:
            Dictionary with local and selected files information
        """
        local_files = self._process_local_files()
        selected_files = self._filter_duplicates(local_files)

        return self._upload_files(selected_files)

    def _process_local_files(self):
        """
        Process and rename local files.

        Returns:
            List of processed files with names and buffers
        """
        file_service = FileService(self.data, self.buffers)
        return file_service.process()

    def _filter_duplicates(self, local_files):
        """
        Remove files that already exist in Directus.

        Args:
            local_files: List of local files to check

        Returns:
            List of files that don't exist in Directus
        """
        directus_files = self.api.fetch_files()
        existing_names = {file["filename_download"] for file in directus_files}

        return [file for file in local_files if file["nome"] not in existing_names]

    def _upload_files(self, selected_files):
        """
        Upload selected files to Directus.

        Args:
            selected_files: List of files to upload
        """
        if selected_files:
            return self.api.upload_files(selected_files)
