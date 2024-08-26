from  uuid import UUID
from dataclasses import dataclass, field
import uuid

@dataclass
class Genre:
    name: str
    is_active: bool = True
    id: UUID = field(default_factory=uuid.uuid4)
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.validate()
        pass

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")
        
        if not self.name: ##len(self.name) == 0:
            raise ValueError("name cannot be an empty string")

    def __str__(self):
        return f"Genre(\n\tid={self.id},\n\tname={self.name},\n\tis_active={self.is_active}\n)"
    
    def __repr__(self) -> str:
        return f"<Genre {self.name} ({self.id})>"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Genre):
            return False
        return self.id == other.id
    
    def change_name(self, name):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

    def add_category(self, category_id: UUID):
        if category_id not in self.categories:
            self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID):
        if category_id in self.categories:
            self.categories.remove(category_id)
        self.validate()