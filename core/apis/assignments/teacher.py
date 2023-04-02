from crypt import methods
import json
from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, GradeAssignmentSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """
    Returns list of Assignment for the provided teacher id
    """
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)

    """
    Serializeing the assignment we received into the AssignmentSchema
    """
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)

    """
    Converting the teacher_assignments_dump to Json for returning a response.
    """
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'])
@decorators.accept_payload
@decorators.auth_principal
def grade_assignments(p, payload):
    """
    Grade an Assignment
    """

    """
    Storing the object in the variable by converting it to the Schema
    """
    data_to_update = GradeAssignmentSchema().load(payload)

    """
    Adding teachers_id and user_id from header for validations reference
    """
    data_to_update.teacher_id = p.teacher_id
    data_to_update.user_id = p.user_id

    """
    Validating some checks and updating the grade of the assignment
    """
    updated_assignment = Assignment.check_and_update_assignment_grade(data_to_update)
    db.session.commit()
    updated_assignment_dump = AssignmentSchema().dump(updated_assignment)


    return APIResponse.respond(data=updated_assignment_dump)
