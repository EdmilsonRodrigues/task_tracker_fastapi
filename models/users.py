


from sqlalchemy import Column, Integer, String
from session import Base

VOWELS = ["a", "e", "i", "o", "u"]


def get_consonants_of_username_doubled(username: str):
    consonants = []
    for letter in username:
        if letter not in VOWELS:
            consonants.append(letter)


class Users(Base):
    __tablename__: "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)


