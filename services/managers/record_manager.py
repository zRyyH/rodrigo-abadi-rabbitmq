class RecordManager:
    """Responsible for creating and managing records in Directus."""

    def __init__(self, api, sheets):
        self.sheets = sheets
        self.api = api

    def create_nfes(self):
        """
        Create NFe records in Directus.

        Args:
            nfes: List of NFe records to create
        """

        nfes = self._remove_duplicate_nfes()

        if nfes:
            self.api.create_nfes(nfes)

    def create_sales(self):
        """
        Create sales records in Directus.

        Args:
            sales: List of sales records to create
        """

        sales = self._remove_duplicate_sales()

        if sales:
            self.api.create_sales(sales)

    def _remove_duplicate_nfes(self):
        """
        Remove NFe records from Directus.

        Args:
            nfes: List of NFe records to remove
        """

        existing_nfes = self.api.fetch_nfes()
        nfes = self.sheets["nfes"]

        existing_keys = {nfe["nfe_key"] for nfe in existing_nfes}
        return [nfe for nfe in nfes if nfe["nfe_key"] not in existing_keys]

    def _remove_duplicate_sales(self):
        """
        Remove sales records from Directus.

        Args:
            sales: List of sales records to remove
        """

        existing_sales = self.api.fetch_sales()
        sales = self.sheets["sales"]

        existing_keys = {sale["sale_id"] for sale in existing_sales}
        return [sale for sale in sales if sale["sale_id"] not in existing_keys]
