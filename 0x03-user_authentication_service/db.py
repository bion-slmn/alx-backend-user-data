"""DB moidule
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict, Union
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''saves a user into the database

        Parameter:
            email : a string representing the email of a user
            hashed_password : a string representing the password
        Return:
            a user object'''
        a_user = User(email=email, hashed_password=hashed_password)
        self._session.add(a_user)
        self._session.commit()
        return a_user

    def find_user_by(self, **kwargs: Dict) -> Union[User, Exception]:
        '''Find a user by the given search criteria.

         Parameters:
            **kwargs : Dict[str, Union[str, int]]
            A dictionary containing search criteria. Keys can include 'id',
            'name', or other attributes of User.

        Returns:
            User: The found user or an exeption'''
        a_user = self._session.query(User).filter_by(**kwargs).one()
        return a_user

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        ''' update a user who has an id user_id with kwargs

        Parameter:
            user_id : id of the the user
            kwargs: items to use to update the user

        Return:
            None'''
        try:
            a_user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                setattr(a_user, key, value)

            self._session.commit()

        except Exception:
            raise ValueError
