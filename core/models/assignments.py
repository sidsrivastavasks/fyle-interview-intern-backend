import enum
from core import db
from core.apis.decorators import Principal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum


class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')
            assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                                    'only assignment in draft state can be edited')

            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, principal: Principal):
        """
        Fetching the assignment matching the provided assignment id
        """
        assignment = Assignment.get_by_id(_id)

        """
        Checking all satisfied conditions on received assignment
        """
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.student_id == principal.student_id, 'This assignment belongs to some other student')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')
        assertions.assert_valid(assignment.state==AssignmentStateEnum.DRAFT, 'only a draft assignment can be submitted')

        assignment.teacher_id = teacher_id
        assignment.state = AssignmentStateEnum.SUBMITTED
        db.session.flush()

        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()

    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        
        """
        Fetching and returning all the assignments 
        that has the teacher_id same as the teacher_id present in the header
        """

        return cls.filter(cls.teacher_id == teacher_id).all()

    @classmethod
    def grade_an_assignment(cls, assignment_to_grade: 'Assignment'):
    
        """
        Fetching the assignment matching the provided assignment id
        """
        assignment = Assignment.get_by_id(assignment_to_grade.id)

        """
        Checking all satisfied conditions on received assignment
        """
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.state != AssignmentStateEnum.DRAFT,'Assignment cannot be graded as its still in Draft state')
        assertions.assert_valid(assignment.state != AssignmentStateEnum.GRADED, 'The Grade has already been given to the student')
        assertions.assert_valid(assignment.teacher_id == assignment_to_grade.teacher_id, f'Assignment {assignment.id} was submitted to teacher {assignment.teacher_id} and not teacher {assignment_to_grade.teacher_id}')
        assertions.assert_valid(assignment_to_grade.grade is not None, 'Grade cannot be empty')
        assertions.assert_valid(assignment_to_grade.grade in GradeEnum.__members__, 'Grade should be one of A, B, C, D')

        """
        Updating the assignment state and grade
        """
        assignment.state = AssignmentStateEnum.GRADED
        assignment.grade = assignment_to_grade.grade
        
        db.session.commit()
        db.session.flush()
        return assignment
