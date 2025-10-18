class DataRelator:
    """Responsible for relating data between different entities."""

    def __init__(self, api):
        self.api = api

    def relate_files_with_nfes(self):
        """
        Relate PDF and XML files with their respective NFes.

        Args:
            nfes: List of NFe records
            files: List of file records from Directus
        """

        nfes_update = []

        files = self.api.fetch_files()
        nfes = self.api.fetch_nfes()

        xml_map = {
            file["filename_download"][:44]: file["id"]
            for file in files
            if file["filename_download"].endswith(".xml")
        }
        pdf_map = {
            file["filename_download"][:44]: file["id"]
            for file in files
            if file["filename_download"].endswith(".pdf")
        }

        for nfe in nfes:
            nfe_key = nfe["nfe_key"]

            nfes_update.append(
                {
                    "id": nfe["id"],
                    "xml_id": xml_map.get(nfe_key),
                    "pdf_id": pdf_map.get(nfe_key),
                }
            )

        self.api.update_nfes(nfes_update)

    def relate_nfes_and_products_with_sales(self):
        """
        Relate NFes with Sales based on business logic.

        Args:
            nfes: List of NFe records
            sales: List of sales records
        """

        sales_update = []

        nfes = self.api.fetch_nfes()
        products = self.api.fetch_products()
        sales = self.api.fetch_sales()

        sku_map = {p["sku"]: p["id"] for p in products}
        sale_or_dispatch_map = {n["sale_or_dispatch"]: n["id"] for n in nfes}

        for sale in sales:
            sales_update.append(
                {
                    "id": sale["id"],
                    "product_id": sku_map.get(sale["sku"]),
                    "nfe_id": sale_or_dispatch_map.get(sale["sale_id"]),
                }
            )

        self.api.update_sales(sales_update)
