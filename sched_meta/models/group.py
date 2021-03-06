import uuid

from sched_meta.models import Base, User

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from sched_meta.models.associations import user_group_association_table


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    admin_id = Column(Integer, ForeignKey('users.id'))
    admin = relationship(User)
    invite_code = Column(String, unique=True, default=lambda: str(uuid.uuid4()))

    users = relationship(User, secondary=user_group_association_table, back_populates="groups")

    def __init__(self, admin: User, title: str):
        self.admin = admin
        self.title = title

    def __repr__(self):
        return f"<Group(id={self.id})>"

    def as_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "admin": self.admin.as_json(),
            "invite_code": self.invite_code
        }
