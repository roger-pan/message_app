from . import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import func
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Data model for Users"""

    __tablename__ = 'User'

    UserID = Column(Integer, primary_key=True)
    username  = Column(String(64), index=True, unique=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    salt = Column(String(64))
    datecreated = Column(DateTime)
    dateupdated = Column(DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_user(dict):

        return User(
            UserId =dict['UserId'],
            username=dict['username'],
            first_name=dict['first_name'],
            last_name =dict['last_name'],
            email=dict['email'],
            password_hash=dict['password_hast'], 
            salt=dict['salt'],
            datecreated=dict['datecreated'],
            dateupdated=dict['dateupdated']         
            )

    def to_user(self):
       """Return object data in easily serializable format"""
       return {
            'UserID'  : self.UserID,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email':self.email,
            'password_hash':self.password_hash,
            'salf':self.salt,
            'datecreated':self.datecreated,
            'dateupdated':self.dateupdated
       }


class Chat(db.Model):
    """ Data Model for Conversations"""

    __tablename__ = 'Chat'

    ChatID = Column(Integer, primary_key=True)
    chatname = Column(String(64), index=True)
    datecreated = Column(DateTime)
    messagessent = Column(Integer)

    @staticmethod
    def from_chat(dict):

        return Chat(
            ChatID =dict['ChatID'],
            chatname =dict['chatname'],
            datecreated =dict['datecreated'],
            messagessent =dict['messagessent']
        )
    
    def to_chat(self):

        return {
            'ChatID' : self.ChatID,
            'chatname': self.chatname,
            'datecreated': self.datecreated,
            'messagessent': self.messagessent
        }


class Chat_User(db.Model):
    """ Data Model for lookup between groups and users"""

    __tablename__ = "Chat_User"
    __tableargs__ = (PrimaryKeyConstraint('UserID', 'ChatID'),
    )

    UserID = Column(Integer, ForeignKey('User.UserID'), primary_key=True)
    ChatID = Column(Integer, ForeignKey('Chat.ChatID'), primary_key=True)

    @staticmethod
    def from_group_user(dict):

        return Group_User(
            UserId =dict['UserID'],
            ChatID =dict['ChatID']
        )

    def to_group_user(self):

        return {
            'UserID': self.UserID,
            'ChatID': self.ChatID
        }


class Message(db.Model):

    __tablename__ = "Message"

    MessageID = Column(Integer, primary_key=True)
    ChatID = Column(Integer, ForeignKey('Chat.ChatID'))
    SenderID = Column(Integer, ForeignKey('User.UserID'))
    content = Column(String)
    timesent = Column(DateTime)

    @staticmethod
    def from_message(dict):

        return Message(

        MessageID =dict['MessageID'],
        ChatID =dict['ChatID'],
        SenderID =dict['SenderID'],
        content =dict['content'],
        timesent =dict['timesent']
        )
    
    def to_message(self):

        return {
        'MessageID': self.MessageID,
        'ChatID': self.ChatID,
        'SenderID': self.SenderID,
        'content': self.content,
        'timesent': self.timesent
        }