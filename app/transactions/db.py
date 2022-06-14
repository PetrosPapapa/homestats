class TransactionDB():
    def getCategories(self):
        raise NotImplementedError

class MockTransactionDB():
    def getCategories(self):
        return [
            "UNKNOWN",
            "BILLS",
            "CAR",
            "CASH",
            "INCOME",
            "OTHER",
            "PHONE",
            "RENT",
            "SCHOOL",
            "SHOPPING",
            "SUPERMARKET",
            "TAX",
            "TICKETS",
            "TRANSFER",
            "UNIVERSITY",
        ]
