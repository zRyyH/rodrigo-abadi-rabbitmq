from zipfile import ZipFile
from pathlib import Path
from io import BytesIO
import requests


class FileService:
    """Service for downloading, extracting and renaming files from zip archives."""

    FILE_SUFFIXES = {"xml": "-procNFe", "pdf": "-DANFE"}
    BASE_PATH = "Emitidas_Mercado_Livre/NF-e de venda"

    def __init__(self, data, buffers):
        self.buffers = buffers
        self.data = data
        self.files = []

    def process(self):
        """
        Main processing pipeline: download, extract and rename files.

        Returns:
            List of processed files with their names and buffers
        """
        self._download_files()
        self._extract_files()
        return self._rename_files()

    def _download_files(self):
        """Download files from provided URLs and store in buffers."""
        for file_key, file_info in self.data["files"].items():
            response = requests.get(file_info["downloadUrl"], timeout=30)
            response.raise_for_status()
            self.buffers[file_key] = BytesIO(response.content)

    def _extract_files(self):
        """Extract PDF and XML files from zip archives."""
        for file_type in ["pdf", "xml"]:
            path = f"{self.BASE_PATH}/{file_type.upper()}/Autorizadas"
            zip_content = self.buffers[f"{file_type}_zip"].getvalue()
            self._extract_from_zip(zip_content, path)

    def _extract_from_zip(self, zip_content, path):
        """
        Extract files from a zip archive that match the given path.

        Args:
            zip_content: Binary content of the zip file
            path: Path prefix to filter files
        """
        with ZipFile(BytesIO(zip_content)) as zip_file:
            normalized_path = Path(path).as_posix()

            for filename in zip_file.namelist():
                if self._is_valid_file(filename, normalized_path):
                    self.files.append(
                        {
                            "nome": Path(filename).name,
                            "buffer": BytesIO(zip_file.read(filename)),
                        }
                    )

    def _is_valid_file(self, filename, path):
        """Check if file is valid (starts with path and is not a directory)."""
        return filename.startswith(path) and not filename.endswith("/")

    def _rename_files(self):
        """Rename all extracted files removing prefixes and suffixes."""
        return [self._rename_single_file(file) for file in self.files]

    def _rename_single_file(self, file):
        """
        Rename a single file by removing unnecessary prefixes and suffixes.

        Args:
            file: Dictionary with 'nome' and 'buffer' keys

        Returns:
            Dictionary with cleaned filename and buffer
        """
        name = file["nome"]

        # Remove prefix before underscore if exists
        if "_" in name:
            name = name.split("_", 1)[1]

        # Remove file type suffix
        extension = name.split(".")[-1]
        name = name.replace(self.FILE_SUFFIXES[extension], "")

        return {"nome": name, "buffer": file["buffer"]}
