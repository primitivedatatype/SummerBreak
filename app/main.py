import csv
import codecs
from fastapi import FastAPI, UploadFile
from models import Transaction
from accounting import Account

app = FastAPI(debug=True)
account = Account()


def hello():
    return "hello"


@app.post("/transactions")
async def submit_transactions(data: UploadFile):
    """
    Accepts, parses, and stores Income and Expense transactions.

    UploadFile is FastAPI's subclass of SpooledTemporaryFile and it is suitable for handling lots of data without overwhelming memory.

    This function uses a DictReader with Codecs.Iterdecode to convert the data into string format (rather than bytes). This technique was sourced from:
    https://stackoverflow.com/questions/70617121/how-to-upload-a-csv-file-in-fastapi-and-convert-it-into-json

    @param: data
    Expects 'multipart/form' (not 'application/json') with newline separated entries containing
    `Date, Type, Amount($), Memo`.
    For example:
        2020-07-01, Expense, 18.77, Gas
        2020-07-04, Income, 40.00, 347 Woodrow
        2020-07-06, Income, 35.00, 219 Pleasant
        2020-07-12, Expense, 49.50, Repairs
    @return: None
    @raises:
        ValueError: if input is invalid
    """
    try:
        hello()
        csv_reader = csv.DictReader(
            codecs.iterdecode(data.file, "utf-8"),
            fieldnames=["date", "xaction_type", "amount", "memo"],
        )
        print("got here")
        for row in csv_reader:
            print("maybe here")
            if not row["date"].startswith("#"):
                xaction = Transaction.parse_obj(row)
                print("just here")
                account.submit_transaction(xaction)
                print("now here")
    finally:
        data.file.close()


@app.get("/report")
async def get_report():
    """
    Generate a report of gross and net revenues, and expenses.
    @return: json object containing:
        {
            "gross-revenue": <amount>,
            "expenses": <amount>,
            "net-revenue": <amount>
        }
    """
    return account.get_account_summary()
