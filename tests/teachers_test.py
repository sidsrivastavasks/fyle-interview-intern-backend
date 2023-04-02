def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1
        assert assignment['state'] == 'SUBMITTED'


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] == 'SUBMITTED'

def test_wrong_api(client, h_teacher_1):
    response = client.get(
        '/teacher/assignment',
        headers=h_teacher_1
    )

    assert response.status_code == 404

    data = response.json
    assert data["error"] == "NotFound"

def test_grade_assignment_graded(client, h_teacher_1):
    """
    Failure case when the Grade has already been given
    """

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    data = response.json
    if response.status_code == 400:
        assert data["error"] == 'FyleError'
        assert data["message"] == 'The Grade has already been given to the student'


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should not allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_teacher_grade_assignment(client, h_teacher_2):
    """
    Teacher Grading an Assignment
    """

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2
        , json={
            "id": 4,
            "grade": "A"
        }
    )

    assert response.status_code == 200
    data = response.json['data']
    assert data['state']=="GRADED"

def test_teacher_submit_assignment(client, h_teacher_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_teacher_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    
    assert response.status_code == 403
    data = response.json

    assert data['error'] == 'FyleError'    