import pytest

from hw.before import CourseManagementSystem, Entity, NotFound


def test_create_teacher():
    cms = CourseManagementSystem()
    teacher = Entity('teacher', 'Ethan Johnson')

    created_id = cms.create_entity(teacher)
    found_teacher = cms.find_entity(created_id)
    assert found_teacher.name == teacher.name
    assert found_teacher.entity_type == teacher.entity_type


def test_create_student():
    cms = CourseManagementSystem()
    student = Entity('student', 'Emma Thompson')

    created_id = cms.create_entity(student)
    found_student = cms.find_entity(created_id)

    assert found_student.name == student.name
    assert found_student.entity_type == student.entity_type


def test_assign_students():
    cms = CourseManagementSystem()

    teacher = Entity('teacher', 'Ethan Johnson')
    teacher_id = cms.create_entity(teacher)

    student_1 = Entity('student', 'Emma Thompson')
    student_1_id = cms.create_entity(student_1)

    student_2 = Entity('student', 'Ava Martinez')
    student_2_id = cms.create_entity(student_2)

    student_3 = Entity('student', 'Sophia Garcia')
    student_3_id = cms.create_entity(student_3)

    cms.assign_student(student_1_id, teacher_id)
    cms.assign_student(student_2_id, teacher_id)
    cms.assign_student(student_3_id, teacher_id)

    assert cms.count_assigned_students(teacher_id) == 3


def test_exceptions():
    cms = CourseManagementSystem()

    with pytest.raises(NotFound):
        cms.list_assigned_students('Mister Anderson')

    with pytest.raises(Exception):
        cms.find_entity(1000)


