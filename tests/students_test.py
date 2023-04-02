def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_student_1(client, h_student_1):

    """
    Creating an Assignment 
    """

    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):

    """
    Submitting an Assignment
    """
    
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_edit_draft_wrong_id(client, h_student_1):
    """
    Student is trying to edit an Assignment that is not present in the database
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 1000,
            "content": "New Edited Content"
        })

    error_response = response.json
    assert response.status_code == 404
    assert error_response["error"] == 'FyleError'

def test_assignment_edit_draft(client, h_student_1):
    """
    Student is trying to edit the draft Assignment
    """

    content = "New Edited Content"
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 5,
            "content": content
        })

    assert response.status_code == 200
    body_response = response.json['data']
    assert body_response["content"] == content


def test_submitted_assignment_edit(client, h_student_1):
    """
    Student Trying to edit the submitted Assignment
    """

    content = 'Try to Edit'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content,
            "id": 1
        })

    assert response.status_code == 400

    data = response.json
    assert data['error'] == "FyleError"
    assert data['message'] == 'only assignment in draft state can be edited'


def test_assingment_resubmitt_error(client, h_student_1):
    """
    Student is Trying to resubmit the assignment
    """

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

def test_assignment_grade_student_1(client, h_student_1):
    """
    Student Trying to Grade an Assignment
    """

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_student_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 403
    data = response.json

    assert data['error'] == 'FyleError'    
