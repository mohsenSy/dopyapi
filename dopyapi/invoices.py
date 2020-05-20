from .resource import Resource

class Invoice(Resource):
    """
    This class represents a single Invoice in Digital Ocean.

    An invoice is generated on the first day of each month. An invoice
    preview is generated daily.

    Attributes:
        invoice_uuid (str): The UUID of the invoice. The canonical reference for the invoice.
        amount (str): Total amount of the invoice, in USD. This will reflect month-to-date usage in the invoice preview.
        invoice_period (str): Billing period of usage for which the invoice is issued, in YYYY-MM format.
        updated_at (datetime): Time the invoice was last updated. This is only included with the invoice preview.
    """
    _url = "customers/my/invoices"
    """
    The URL used for the invoices endpoint
    """
    _plural = "invoices"
    """
    The dictionary key used when fetching multiple invoices
    """
    _single = "invoice"
    """
    The dictionary key used when fetching a single invoice
    """
    _fetch_attrs = ["invoice_uuid"]
    """
    These attributes can be used to fetch an invoice by their value
    """
    _static_attrs = ["amount", "invoice_period", "updated_at"]
    """
    These attributes are set by Digital Ocean for an invoice and cannot be changed directly
    """
    _dynamic_attrs = []
    """
    These attributes can be used when creating a new invoice or updating an existing one
    """
    _action_attrs = []
    """
    Actions that can be called on invoices
    """
    _delete_attr = ""
    """
    This is the name of the attribute used to delete invoice by its value
    """
    _update_attr = ""
    """
    This is the name of the attribute used to update invoices by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "invoice_uuid"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "invoice"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(Invoice)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Invoice uuid: {self.invoice_uuid} amount: {self.amount}>"
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of invoices as defined by its arguments

        Arguments:
            page (int): The page to fetch from all invoices (defaults 1)
            per_page (int): The number of invoices per a single page (defaults 20)

        Returns:
            list: A list of invoices
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        invoices = super().list(**kwargs)
        return [cls(x) for x in invoices]
    def getCSV(self):
        """
        Get a CSV summary of the invoice

        Return:
            str: CSV data as a string
        """
        url = f"{self._url}/{self.invoice_uuid}/csv"
        data = self.get(url=url)
        data = data.decode("utf-8")
        return data
    def getPDF(self):
        """
        Get a PDF summary of the invoice

        Return:
            bytes: A bytes object for the PDF data.
        """
        url = f"{self._url}/{self.invoice_uuid}/pdf"
        data = self.get(url=url)
        return data
    def saveCSV(self, file=None):
        """
        Save a CSV summary to a file.

        Args:
            file: The name of the file to save CSV data to it, default is {invoice_period}.csv
        """
        if file is None:
            file = f"{self.invoice_period}.csv"
        with open(file, "w") as f:
            csv = self.getCSV()
            f.write(csv)
    def savePDF(self, file=None):
        """
        Save a PDF summary to a file.

        Args:
            file: The name of the file to save CSV data to it, default is {invoice_period}.pdf
        """
        if file is None:
            file = f"{self.invoice_period}.pdf"
        with open(file, "wb") as f:
            pdf = self.getPDF()
            f.write(pdf)

class InvoiceItem(Resource):
    """
    This class represents a single Invoice item in Digital Ocean.

    Invoice Items show details for each invoice, such as product names,
    their usage time and their price.

    Attributes:
        product (str): Name of the product being billed in the invoice item.
        resource_uuid (str): UUID of the resource billing in the invoice item if available.
        resource_id (str): ID of the resource billing in the invoice item if available.
        group_description (str): Description of the invoice item when it is a grouped set of usage, such as DOKS or databases.
        description (str): Description of the invoice item.
        amount (str): Billed amount of this invoice item. Billed in USD.
        duration (str): Duration of time this invoice item was used and subsequently billed.
        duration_unit (str): Unit of time for duration.
        start_time (datetime): Time the invoice item began to be billed for usage.
        end_time (datetime): Time the invoice item stoped being billed for usage.
        project_name (str): Name of the DigitalOcean Project this resource belongs to.
    """
    _url = "customers/my/invoices/{}"
    """
    The URL used for the invoice items endpoint
    """
    _plural = "invoice_items"
    """
    The dictionary key used when fetching multiple invoice items
    """
    _single = "invoice_item"
    """
    The dictionary key used when fetching a single invoice item
    """
    _fetch_attrs = []
    """
    These attributes can be used to fetch an invoice item by their value
    """
    _static_attrs = ["product", "resource_uuid", "resource_id", "group_description", "description", "amount", "duration", "duration_unit", "start_time", "end_time", "project_name"]
    """
    These attributes are set by Digital Ocean for an invoice item and cannot be changed directly
    """
    _dynamic_attrs = []
    """
    These attributes can be used when creating a new invoice item or updating an existing one
    """
    _action_attrs = []
    """
    Actions that can be called on invoice item
    """
    _delete_attr = ""
    """
    This is the name of the attribute used to delete invoice item by its value
    """
    _update_attr = ""
    """
    This is the name of the attribute used to update invoice items by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "resource_uuid"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "invoice_item"
    """
    This holds the type of resource.
    """
    def __init__(self, invoice_uuid, data=None):
        super().__init__(InvoiceItem)
        self._url = self._url.format(invoice_uuid)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<InvoiceItem product: {self.product} amount: {self.amount}>"
    @classmethod
    def list(cls, invoice_uuid, **kwargs):
        """
        This method returns a list of invoice items as defined by its arguments

        Arguments:
            page (int): The page to fetch from all invoice items (defaults 1)
            per_page (int): The number of invoice items per a single page (defaults 20)

        Returns:
            list: A list of invoice items
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = cls._url.format(invoice_uuid)
        invoice_items = super().list(url=url, **kwargs)
        return [cls(invoice_uuid, x) for x in invoice_items]
    @classmethod
    def listPreview(cls, **kwargs):
        """
        This method returns a list of invoice items for the preview invoice generated daily
        as defined by its arguments

        Arguments:
            page (int): The page to fetch from all invoice items (defaults 1)
            per_page (int): The number of invoice items per a single page (defaults 20)

        Returns:
            list: A list of invoice items
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = cls._url.format("preview")
        invoice_items = super().list(url=url, **kwargs)
        return [cls("preview", x) for x in invoice_items]

class InvoiceSummary(Resource):
    """
    This class represents a single Invoice summary in Digital Ocean.

    Attributes:
        invoice_uuid (str): UUID of invoice.
        billing_period (str): Billing period of usage for which the invoice is issued, in YYYY-MM format.
        amount (str): Total amount of the invoice, in USD. This will reflect month-to-date usage in the invoice preview.
        user_name (str): Name of the DigitalOcean customer being invoiced.
        user_billing_address (dict): The billing address of the customer being invoiced.
        user_company (str): Company of the DigitalOcean customer being invoiced, if set.
        user_email (str): Email of the DigitalOcean customer being invoiced.
        product_charges (dict): A summary of the product usage charges contributing to the invoice. This will include an amount, and grouped aggregates by resource type under the items key.
        overages (dict): A summary of the overages contributing to the invoice.
        taxes (dict): A summary of the taxes contributing to the invoice.
        credits_and_adjustments (dict): A summary of the credits and adjustments contributing to the invoice.
    """
    _url = "customers/my/invoices/{}/summary"
    """
    The URL used for the invoice summary endpoint
    """
    _plural = "invoice_summary"
    """
    The dictionary key used when fetching multiple invoice summaries
    """
    _single = "invoice_summary"
    """
    The dictionary key used when fetching a single invoice summary
    """
    _fetch_attrs = []
    """
    These attributes can be used to fetch an invoice summary item by their value
    """
    _static_attrs = ["invoice_uuid", "billing_period", "amount", "user_name", "user_billing_address", "user_company", "user_email", "product_charges", "overages", "taxes", "credits_and_adjustments"]
    """
    These attributes are set by Digital Ocean for an invoice summary and cannot be changed directly
    """
    _dynamic_attrs = []
    """
    These attributes can be used when creating a new invoice summary or updating an existing one
    """
    _action_attrs = []
    """
    Actions that can be called on invoice summary
    """
    _delete_attr = ""
    """
    This is the name of the attribute used to delete invoice summary by its value
    """
    _update_attr = ""
    """
    This is the name of the attribute used to update invoice summary by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "invoice_uuid"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "invoice_summary"
    """
    This holds the type of resource.
    """
    def __init__(self, invoice_uuid, data=None):
        super().__init__(InvoiceSummary)
        self._url = self._url.format(invoice_uuid)
        if data is None:
            data = self.get(self._url)
        self._update({self._single: data})
    def __repr__(self):
        return f"<InvoiceSummary billing period: {self.billing_period} amount: {self.amount}>"
