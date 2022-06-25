host = "127.0.0.1"

db = {
    "host": "db.host",
    "port": 1234,
    "database": "dbname",
    "username": "uname",
    "password": "password"
    "transactions_tbl": "transactions",
    "energy_tbl": "energy"
}

energy = {
    "address": "someaddress"
}

transactions = {
    "categories": [
        "UNKNOWN",
        "BILLS",
        "CASH",
        "INCOME",
        "OTHER",
        "RENT",
        "SCHOOL",
        "SHOPPING",
        "SUPERMARKET",
        "TAX",
        "TRANSFER",
    ],

    "non_expense_categories": [
        'INCOME', 
        'TRANSFER', 
    ],

    "firstDayOfMonth": 17
}
