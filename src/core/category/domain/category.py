import uuid
from dataclasses import dataclass, field

@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")
        
        if not self.name: ##len(self.name) == 0:
            raise ValueError("name cannot be an empty string")

    def __str__(self):
        return f"Category(\n\tid={self.id},\n\tname={self.name},\n\tdescription={self.description},\n\tis_active={self.is_active}\n)"
    
    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.id})>"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self.id == other.id
    
    def update_category(self, name, description):
        self.name = name
        self.description = description
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
