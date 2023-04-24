# SummerBreak

## Environment Setup
* Install and Start Docker
https://docs.docker.com/get-docker/

## Build and run unit tests in a container
```
make clean; make build && make test
```

## Unit Test Coverage
The Makefile `test-coverage` target is under construction.
The following two commands work in the meantime to see coverage reports.
```
docker run -it --rm -w /app summer-break
coverage run -m pytest . && coverage report -m
```

## Build and run the webserver in a container:
```
make clean; make build && make run
```

# Usage

## POST transaction data from a file on disk (ie: data.csv)
```
curl -X POST http://127.0.0.1:5000/transactions \
    -F "data=@data.csv" -H "Content-Type: multipart/form-data"
```

## GET report of gross-revenue, expenses, and net-revenue
```
curl -X GET http://127.0.0.1:5000/report
```

# Engineering Approach
This web server is built using the FastAPI framework for async API endpoints and Pydantic framework for data models and data validation.

A single global `Account` instance supports one user for receipts related to one business. 

The `submit_transactions` function uses an iterator over a `SpooledTemporaryFile` to call `Account.submit_transaction` on one transaction at a time. If the `Account` class is modified to persist each transaction to disk, then a large amount of transactions could be submitted without overutilizing memory resources.

Docker is used to make project builds reproducible.


## Shortcomings and Assumptions
The `Account` instance and its data are held in memory, so the state only lasts as long as the process runs. For example, a user can get a report for all prepared receipts and transactions and multiple Post requests can be made. However, if the process dies then the account data is lost.
 
If a `POST /transactions` request is made with several entries and one is invalid, then all transactions in that request will be rejected.

The `GET /report` endpoint does not indicate the number of transactions that were accounted for in a given report. This is because the Account object does not keep track.

# Future refinements and features
* Return the number of transactions processed from the POST /transactions endpoint.
* Improve code coverage: test that data files are always closed from finally block in POST request
* Money: Implement a clean way to handle financial values to mitigate floating point errors 
* Authentication: A minimal method is to return a UUID from a POST request could be reused to post additional transactions to the same account, and receive the related report. More elaborate authentication methods are also available if needed.
* Clear Data: delete all data related to the account, maybe based on a provided UUID
* Persist transaction data: 
    This could be persisted per memo (category / job address) to support more tailored reports. The accounting.Account class can handle database interactions to submit data and perform queries to address questions about the data like:
    1. Calculate total summer income from job named "347 Woodrow".
    2. Calculate total expense for gas during the month of July.
    Postgres could be a good fit for queries like these.
