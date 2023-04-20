# SummerBreak

# Build (inside a virtualenv)
```
    pip install -r requirements.txt
```

# Start webserver:
```
    python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 5001
```

# POST
```
    curl -X POST http://127.0.0.1:5001/transactions  -F "data=@data.csv" -H "Content-Type: multipart/form-data"
```

# GET
```
    curl -X GET http://127.0.0.1:5001/report
```
