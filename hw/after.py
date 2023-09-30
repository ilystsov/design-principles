from collections import defaultdict
from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod


@dataclass
class Entity:
    entity_type: str
    name: str


class CourseEntitiesManagement:
    def __init__(self):
        self.id = 0
        self.entities_table = {}

    def create_entity(self, entity: Entity) -> int:
        id = self.id
        type = entity.entity_type
        if type not in self.entities_table:
            self.entities_table[type] = {}
        self.entities_table[type][id] = entity
        self.id += 1
        return id


class AssignEntities(ABC):
    @abstractmethod
    def assign_entity(self, entity_to_assign, base_entity):
        pass


class ListAssignedEntities(ABC):
    @abstractmethod
    def list_assigned_entities(self, entity_name):
        pass


class AssignTeacherStudents(AssignEntities):
    def __init__(self):
        self.student_teacher_assignment_table = defaultdict(list)

    def assign_entity(self, student_id: int, teacher_id: int):
        self.student_teacher_assignment_table[teacher_id].append(student_id)


class ListTeacherStudents(ListAssignedEntities):
    def __init__(self, entities_table, assignment_table):
        self.entities_table = entities_table
        self.assignment_table = assignment_table

    def list_assigned_entities(self, teacher_name: str) -> List[str]:
        for teacher_id, teacher in self.entities_table['teacher'].items():
            if teacher.name == teacher_name:
                return self.assignment_table[teacher_id]
        raise KeyError('Teacher not found')
