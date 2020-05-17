from .resource import Resource
from .common import _create_object
class Balance(Resource):
    """
    This class holds information about customer's balance

    Attributes:
        month_to_date_balance (str): Balance as of the generated_at time.
            This value includes the account_balance and month_to_date_usage.
        account_balance (str): Current balance of the customer's most recent
            billing activity. Does not reflect month_to_date_usage.
        month_to_date_usage (str): Amount used in the current billing
            period as of the generated_at time.
        generated_at (datetime.datetime): The time at which balances were
            most recently generated.
    """
    _url = "customers/my/balance"
    """
    The URL used for the balance endpoint
    """
    _plural = ""
    """
    Not used
    """
    _single = ""
    """
    Not used
    """
    _fetch_attrs = []
    """
    Not used
    """
    _static_attrs = ["month_to_date_balance", "account_balance", "month_to_date_usage", "generated_at"]
    """
    These attributes are set by Digital Ocean for the balance and cannot be changed directly
    """
    _dynamic_attrs = []
    """
    Not used
    """
    _action_attrs = []
    """
    Not actions
    """
    _delete_attr = ""
    """
    Cannot delete anything
    """
    _update_attr = ""
    """
    Cannot update anything
    """
    _action_attr = ""
    """
    Cannot call actions
    """
    _id_attr = "month_to_date_balance"
    """
    This is only a placceholder to not give errors later
    """
    _resource_type = "balance"
    """
    This holds the type of resource.
    """
    def __init__(self):
        super().__init__(Balance)
        self._update(self.get(self._url))
    def _update(self, data):
        for k, v in data.items():
            if k in self._static_attrs:
                self.__dict__[k] = _create_object(k, v)
    def __repr__(self):
        return f"<Balance monthly to date usage: {self.month_to_date_usage}>"


class BillingHistory(Resource):
    """
    This class can be used to retrieve the billing history for customers

    Attributes:
        description (str): Description of the billing history entry.
        ammount (str): Amount of the billing history entry.
        invoice_id (str): ID of the invoice associated with the billing history entry, if applicable.
        invoice_uuid (str): UUID of the invoice associated with the billing history entry, if applicable.
        date (datetime.datetime): Time the billing history entry occured.
        type (str): Type of billing history entry.
    """
    _url = "customers/my/billing_history"
    """
    The URL used for the billing history endpoint
    """
    _plural = "billing_history"
    """
    The dictionary key used when fetching billing history
    """
    _single = "billing_history"
    """
    The dictionary key used when fetching billing history
    """
    _fetch_attrs = []
    """
    Not used
    """
    _static_attrs = ["description", "amount", "invoice_id", "invoice_uuid", "date", "type"]
    """
    These attributes are set by Digital Ocean for the billing history and cannot be changed directly
    """
    _dynamic_attrs = []
    """
    Not used
    """
    _action_attrs = []
    """
    Not actions
    """
    _delete_attr = ""
    """
    Cannot delete anything
    """
    _update_attr = ""
    """
    Cannot update anything
    """
    _action_attr = ""
    """
    Cannot call actions
    """
    _id_attr = "invoice_id"
    """
    This is only a placceholder to not give errors later
    """
    _resource_type = "billing_history"
    """
    This holds the type of resource.
    """

    def __init__(self, data=None):
        super().__init__(BillingHistory)
        if data is not None:
            self._update({self._single: data})
    def __str__(self):
        return f"<BillingHistory type:{self.type}, invoice_id:{self.invoice_id}>"
    def __repr__(self):
        return f"<BillingHistory type:{self.type}, invoice_id:{self.invoice_id}>"
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of billing history as defined by its arguments

        Arguments:
            page (int): The page to fetch from all history (defaults 1)
            per_page (int): The number of items per a single page (defaults 20)

        Returns:
            list: A list of billing history
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        bills = super().list(**kwargs)
        return [cls(x) for x in bills]
