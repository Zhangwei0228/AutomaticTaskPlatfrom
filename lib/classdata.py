from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Table, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 添加 File 类
class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    path = Column(String(255))

    # 添加与 user 的多对多关系
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="files")

    def __repr__(self):
        return f"File(id={self.id}, name={self.name}, path={self.path})"


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    # 添加与user的多对多关系
    path = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="roles")

    def __repr__(self):
        return f"Roles(id={self.id}, name={self.name})"


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    path = Column(String(255))

    # 添加与user的多对多关系
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="templates")

    def __repr__(self):
        return f"Template(id={self.id}, name={self.name})"


# 在User类中添加roles和templates关系
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    name = Column(String(20))
    nickname = Column(String(40))
    email = Column(String(40))
    ansible_logs = relationship("AnsibleLog", back_populates="user", cascade="all, delete-orphan")
    # 添加关系
    hosts = relationship("HostMachine", back_populates="user", cascade="all, delete-orphan")
    playbooks = relationship("AnsiblePlaybook", back_populates="user", cascade="all, delete-orphan")
    ansible_configs = relationship("AnsibleConfig", back_populates="user", cascade="all, delete-orphan")
    adhocs = relationship("Adhoc", back_populates="user", cascade="all, delete-orphan")
    templates = relationship("Template", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("Roles", back_populates="user", cascade="all, delete-orphan")
    files = relationship("File", back_populates="user", cascade="all, delete-orphan")
    models = relationship("AnsibleModel", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"


class HostMachine(Base):
    __tablename__ = "host_machine"

    id = Column(Integer, primary_key=True)
    hostname = Column(String(50))
    ip = Column(String(128))
    ssh_port = Column(Integer(), default=22)

    # 添加关系
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates='hosts')
    hosts = relationship("HostUser", back_populates="host", cascade="all, delete-orphan")
    group_id = Column(Integer, ForeignKey("group.id"))
    group = relationship("Group", back_populates='hosts')

    def __repr__(self):
        return f"HostMachine(id={self.id}, hostname={self.hostname}, ip={self.ip})"


class HostUser(Base):
    __tablename__ = "host_users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(100))
    host_id = Column(Integer, ForeignKey("host_machine.id"))
    host = relationship("HostMachine", back_populates='hosts')


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    hosts = relationship("HostMachine", back_populates="host_machine")
    parent_group_id = Column(Integer, ForeignKey('group.id'))
    parent_group = relationship("Group", remote_side="Group.id", back_populates="child_groups")
    child_groups = relationship("Group", back_populates="parent_group")

    def __repr__(self):
        return f"Group(id={self.id}, name={self.name})"


class AnsiblePlaybook(Base):
    __tablename__ = "ansible_playbook"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    path = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    # 添加关系
    user = relationship("User", back_populates="playbooks")

    def __repr__(self):
        return f"AnsiblePlaybook(id={self.id}, name={self.name}, path={self.path})"


class AnsibleConfig(Base):
    __tablename__ = "ansible_config"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)

    # Ansible配置项
    inventory = Column(String(255))
    remote_user = Column(String(50))
    become = Column(Boolean)
    become_method = Column(String(50))
    become_user = Column(String(50))
    become_ask_pass = Column(Boolean)
    roles_path = Column(String(255))
    log_path = Column(String(255))
    # 添加与用户的一对一关系
    user = relationship("User", back_populates="ansible_configs")

    def __repr__(self):
        return f"AnsibleConfig(id={self.id}, user_id={self.user_id}, remote_user={self.remote_user}, private_key_file={self.private_key_file}, ...)"


class AnsibleLog(Base):
    __tablename__ = "ansible_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(String(255))

    # 添加与用户的一对多关系
    user = relationship("User", back_populates="ansible_logs")

    def __repr__(self):
        return f"AnsibleLog(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp}, message={self.message})"


class Adhoc(Base):
    __tablename__ = "adhoc"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    content = Column(Text())
    description = Column(String(255))
    # 添加与 user 的多对多关系
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="adhocs")

    def __repr__(self):
        return f"Adhoc(id={self.id}, name={self.name})"


class AnsibleModel(Base):
    __tablename__ = "ansible_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    path = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="adhocs")


class AnsibleActionPlugins(Base):
    __tablename__ = "ansible_action_plugins"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    path = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="adhocs")
