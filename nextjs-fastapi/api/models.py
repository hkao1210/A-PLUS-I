from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Association table for many-to-many relationship between students and classes
student_class_association = Table('student_class_association', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('class_id', Integer, ForeignKey('classes.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)  # 'teacher' or 'admin'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    classes = relationship("Class", back_populates="teacher")

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    teacher = relationship("User", back_populates="classes")
    tests = relationship("Test", back_populates="class")
    students = relationship("Student", secondary=student_class_association, back_populates="classes")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    classes = relationship("Class", secondary=student_class_association, back_populates="students")
    test_results = relationship("TestResult", back_populates="student")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    class_id = Column(Integer, ForeignKey("classes.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    class_ = relationship("Class", back_populates="tests")
    questions = relationship("Question", back_populates="test")
    test_results = relationship("TestResult", back_populates="test")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    question_text = Column(String)
    question_type = Column(String)  # e.g., 'multiple_choice', 'short_answer', 'essay'
    correct_answer = Column(String)  # For multiple choice or short answer
    points = Column(Integer)

    test = relationship("Test", back_populates="questions")

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    score = Column(Integer)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    test = relationship("Test", back_populates="test_results")
    student = relationship("Student", back_populates="test_results")
    answers = relationship("Answer", back_populates="test_result")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    test_result_id = Column(Integer, ForeignKey("test_results.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(String)
    is_correct = Column(Boolean)
    points_earned = Column(Integer)

    test_result = relationship("TestResult", back_populates="answers")
    question = relationship("Question")
class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(String, primary_key=True)
    filename = Column(String)
    file_path = Column(String)  # Path to the stored file
    upload_date = Column(DateTime(timezone=True), server_default=func.now())