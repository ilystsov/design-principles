from collections import defaultdict
from dataclasses import dataclass
from typing import List


class NotFound(Exception):                          # Occam's razor. It is not necessary to create a separate class
    pass                                            # for throwing an exception. It is better to use KeyError exception.


@dataclass
class Entity:
    entity_type: str
    name: str


class IndexGenerator:                               # KISS. It is not necessary to create a separate class
    def __init__(self):                             # to simply increment index by 1.
        self.current = 0

    def generate_index(self) -> int:
        self.current = self.current + 1
        return self.current


class CourseManagementSystem:                       # Single responsibility. The class needs to be divided
    def __init__(self):                             # into separate classes (i.e. class which creates entities
        self.igen = IndexGenerator()                # and class which assigns them)
        self.teachers_table = {}
        self.students_table = {}
        self.student_teacher_assignment_table = defaultdict(list)

    def next_index(self):                           # KISS. It is not necessary to create a separate function
        return self.igen.generate_index()           # to simply increment index by 1.

    def create_entity(self, entity: Entity) -> int:
        next_index = self.next_index()
        if entity.entity_type == 'teacher':             # Open-closed. If we wanted to add more entities (i.e. course
            self.teachers_table[next_index] = entity    # administrators), we would need to modify the code.
        else:
            self.students_table[next_index] = entity
        return next_index

    def find_entity(self, entity_id) -> Entity:     # YAGNI. There was no request to implement this function in the task
        if entity_id in self.teachers_table:        # and it is not used meaningfully anywhere in the code.
            return self.teachers_table[entity_id]   # Open-closed. If we wanted to add more entities' tables,
                                                    # we would need to modify the code.
        return self.students_table[entity_id]

    def assign_student(self, s_entity_id: int, t_entity_id: int):
        teacher = self.find_entity(t_entity_id)     # YAGNI. These variables are not used in the function.
        student = self.find_entity(s_entity_id)     # Open-closed. If we wanted to add more entities, we would
                                                    # need to modify the code.
        self.student_teacher_assignment_table[t_entity_id].append(s_entity_id)

    def count_assigned_students(self, entity_id: int) -> int:       # YAGNI. There was no request to implement
        teacher = self.find_entity(entity_id)                       # this function in the task. The 'teacher' variable
                                                                    # is not used in the code.
        return len(self.student_teacher_assignment_table[entity_id])

    def list_assigned_students(self, name: str) -> List[str]:
        for k, v in self.teachers_table.items():                    # Open-closed. We must modify the code if we
            if v.name == name:                                      # want to add more entities.
                return self.student_teacher_assignment_table[k]
        raise NotFound('teacher not found')