from .base import Base


class Venue(Base):
    name: str
    city: str | None
