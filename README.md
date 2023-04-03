# Fyle Backend Challenge

### My tasks

1. Add missing APIs mentioned [here](./Application.md#Missing-APIs) and get the automated tests to pass
2. Add a test for grading API
3. All tests should pass
4. Get the test coverage to 94% or above

## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```

### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```

### Start Server

```
bash run.sh
```

### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```

---

## Available API's for Teachers

### Auth

-   header: "X-Principal"
-   value: {"user_id":3, "teacher_id":1}

For APIs to work we need a principal header to establish identity and context

### GET /teacher/assignments

#### List all assignments submitted to this teacher

```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:14:01.584644"
        }
    ]
}
```

### POST /teacher/assignments/grade

#### Grade an assignment

```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

payload:
{
    "id":  1,
    "grade": "A"
}

response:
{
    "data": {
        "content": "ESSAY T1",
        "created_at": "2021-09-17T03:14:01.580126",
        "grade": "A",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2021-09-17T03:20:42.896947"
    }
}
```

---
