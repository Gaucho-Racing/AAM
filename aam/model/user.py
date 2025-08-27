from datetime import datetime

from pydantic import BaseModel, Field


class Subteam(BaseModel):
    """Represents a subteam that users can belong to."""

    id: str
    name: str
    created_at: datetime


class User(BaseModel):
    """Represents a user from the Sentinel API."""

    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    gender: str
    birthday: str
    graduate_level: str
    graduation_year: int
    major: str
    shirt_size: str
    jacket_size: str
    sae_registration_number: str
    avatar_url: str
    verified: bool
    subteams: list[Subteam] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    updated_at: datetime
    created_at: datetime

    def __str__(self) -> str:
        """String representation of the user."""
        return f"({self.id}) {self.first_name} {self.last_name} [{self.email}]"

    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles

    def has_subteam(self, subteam_name: str) -> bool:
        """Check if user belongs to a specific subteam."""
        return any(s.name == subteam_name for s in self.subteams)

    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.has_role("d_admin")

    def is_officer(self) -> bool:
        """Check if user is an officer."""
        return self.has_role("d_officer")

    def is_lead(self) -> bool:
        """Check if user is a lead."""
        return self.has_role("d_lead")

    def is_special_advisor(self) -> bool:
        """Check if user is a special advisor."""
        return self.has_role("d_special_advisor")

    def is_inner_circle(self) -> bool:
        """Check if user is in the inner circle (admin, officer, or lead)."""
        return (
            self.is_admin()
            or self.is_officer()
            or self.is_lead()
            or self.is_special_advisor()
        )
