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
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)

    # Serializeing the assignment we received into the AssignmentSchema
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)

    return APIResponse.respond(data=teacher_assignments_dump)



@teacher_assignments_resources.route('/assignments/grade', methods=['POST'])
@decorators.accept_payload
@decorators.auth_principal
def grade_an_assignments(p, payload):

    assignment_to_grade = GradeAssignmentSchema().load(payload)    

    # Adding teachers_id and user_id fields from X-Principal header for validations reference
    assignment_to_grade.teacher_id = p.teacher_id
    assignment_to_grade.user_id = p.user_id

    # Grading an assignment based on the input received
    updated_assignment = Assignment.grade_an_assignment(assignment_to_grade)
    updated_assignment_dump = AssignmentSchema().dump(updated_assignment)


    return APIResponse.respond(data=updated_assignment_dump)
