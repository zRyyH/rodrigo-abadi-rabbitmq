from integration.directus import Directus


class ApiService:
    def __init__(self):
        self.directus = Directus()

    def fetch_files(self):
        """Fetch all files from Directus."""
        result = self.directus.get(
            collection="files",
            params={"limit": -1, "fields": ["filename_download", "id"]},
        )
        return result["data"]

    def fetch_products(self):
        """Fetch all products from Directus."""
        result = self.directus.get(
            collection="items/products", params={"limit": -1, "fields": ["sku", "id"]}
        )
        return result["data"]

    def fetch_nfes(self):
        """Fetch all NFes from Directus."""
        result = self.directus.get(
            collection="items/nfes",
            params={"limit": -1},
        )
        return result["data"]

    def update_nfes(self, nfes):
        result = self.directus.update(
            collection="nfes",
            data=nfes,
        )
        return result["data"]

    def update_sales(self, sales):
        result = self.directus.update(
            collection="sales",
            data=sales,
        )
        return result["data"]

    def fetch_sales(self):
        """Fetch all sales from Directus."""
        result = self.directus.get(
            collection="items/sales",
            params={"limit": -1},
        )
        return result["data"]

    def create_nfes(self, nfes):
        """Create NFe records in Directus."""
        return self.directus.create("nfes", nfes)

    def create_sales(self, sales):
        """Create sales records in Directus."""
        return self.directus.create("sales", sales)

    def upload_files(self, files):
        """Upload files to Directus."""
        if not files:
            raise ValueError("Nenhum arquivo foi fornecido para upload.")

        return self.directus.uploadFiles(files)
