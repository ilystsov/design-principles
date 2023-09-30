import pytest

from hw.after import CourseEntitiesManagement, Entity, AssignTeacherStudents, ListTeacherStudents


def test_create_teacher():
    cem = CourseEntitiesManagement()
    teacher = Entity('teacher', 'Ethan Johnson')

    created_id = cem.create_entity(teacher)
    found_teacher = cem.entities_table['teacher'][created_id]

    assert found_teacher.name == teacher.name
    assert found_teacher.entity_type == teacher.entity_type


def test_create_student():
    cem = CourseEntitiesManagement()
    student = Entity('student', 'Emma Thompson')

    created_id = cem.create_entity(student)
    found_student = cem.entities_table['student'][created_id]

    assert found_student.name == student.name
    assert found_student.entity_type == student.entity_type


def test_assign_students():
    ats = AssignTeacherStudents()
    cem = CourseEntitiesManagement()
    teacher = Entity('teacher', 'Ethan Johnson')
    teacher_id = cem.create_entity(teacher)

    student_1 = Entity('student', 'Emma Thompson')
    student_1_id = cem.create_entity(student_1)

    student_2 = Entity('student', 'Ava Martinez')
    student_2_id = cem.create_entity(student_2)

    student_3 = Entity('student', 'Sophia Garcia')
    student_3_id = cem.create_entity(student_3)

    ats.assign_entity(student_1_id, teacher_id)
    ats.assign_entity(student_2_id, teacher_id)
    ats.assign_entity(student_3_id, teacher_id)

    assert len(ats.student_teacher_assignment_table[teacher_id]) == 3


def test_exception():
    lts = ListTeacherStudents({}, {})

    with pytest.raises(KeyError):
        lts.list_assigned_entities('Mister Anderson')



