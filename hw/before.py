from collections import defaultdict
from dataclasses import dataclass
from typing import List


class NotFound(Exception):
    pass


@dataclass
class Entity:
    entity_type: str
    name: str


class IndexGenerator:
    def __init__(self):
        self.current = 0

    def generate_index(self) -> int:
        self.current = self.current + 1
        return self.current


class CourseManagementSystem:
    def __init__(self):
        self.igen = IndexGenerator()
        self.teachers_table = {}
        self.students_table = {}
        self.student_teacher_assignment_table = defaultdict(list)

    def next_index(self):
        return self.igen.generate_index()

    def create_entity(self, entity: Entity) -> int:
        next_index = self.next_index()
        if entity.entity_type == 'teacher':
            self.teachers_table[next_index] = entity
        else:
            self.students_table[next_index] = entity
        return next_index

    def find_entity(self, entity_id) -> Entity:
        if entity_id in self.teachers_table:
            return self.teachers_table[entity_id]

        return self.students_table[entity_id]

    def assign_student(self, s_entity_id: int, t_entity_id: int):
        teacher = self.find_entity(t_entity_id)
        student = self.find_entity(s_entity_id)

        self.student_teacher_assignment_table[t_entity_id].append(s_entity_id)

    def count_assigned_students(self, entity_id: int) -> int:
        teacher = self.find_entity(entity_id)

        return len(self.student_teacher_assignment_table[entity_id])

    def list_assigned_students(self, name: str) -> List[str]:
        for k, v in self.teachers_table.items():
            if v.name == name:
                return self.student_teacher_assignment_table[k]
        raise NotFound('teacher not found')