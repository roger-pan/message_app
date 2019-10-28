from flask import Flask, jsonify, render_template
from flask import request, Blueprint
import sqlalchemy
from . import db
from application import models

MessageAPI = Blueprint("messages_api", __name__)
@MessageAPI.route('/api/chats/<ChatID>/messages?UserID=<UserID>', methods=['GET'])
def get_messages():
    """
    Gets all the messages for a user_id and chat_id
    """

    result = db.session.execute(
        '''
        SELECT 
          m.MessageID
         ,m.ChatID
         ,m.SenderID
         ,m.content
         ,m.timesent 
        FROM 
          messages AS m 
        INNER JOIN 
          group_users AS gu 
        ON 
          gu.ChatID = m.ChatID 
        WHERE 
          m.ChatID = :chat_id 
        AND 
          gu.UserID = :user_id'
        '''
        , {chat_id: ChatID, user_id: UserID }
    )
    message_dict = [row.to_message() for row in result]
    return jsonify(message_dict)


@MessageAPI.route('/api/chats/<ChatID>/messages?UserID=<UserID>', methods=['POST'])
def send_messages():
    """
    Allows a user to send a message. Takes as arguments GroupID, SenderID and Content
    """
    if request.json: # If there is data in the POST request
        for row in request.json:
            message = row.to_message() #
            result = db.session.execute(
            '''
            INSERT INTO messages AS m (m.GroupID, m.SenderID, m.content) 
            VALUES (:chat_id, :sender_id, :content)
            '''
        ,{chat_id: message['ChatID'], sender_id: message['SenderID'], content: message['content']}
            )

        db.session.commit() # Comitting the changes
        return "Success: You created a new message"

@MessageAPI.route('/api/chats/<ChatID>/messages?UserID=<UserID>', methods=['PUT'])
def edit_message():
    """
    Edit a message. Takes MessageID and content as parameters.
    """

    if request.json:
        for row in request.json:
            message = row.to_message()
            result = db.session.execute(
                '''
                UPDATE messages AS m 
                SET m.content = :content
                WHERE m.MessageID = :message_id
                '''
                , {content: message['content'], message_id: message['MessageID']}
            )
        db.session.commit()
        return "Success: You edited a message"

@MessageAPI.route('/api/chats/<ChatID>/messages?UserID=<UserID>', methods=['DELETE'])
def delete_message():
    """
    Deletes a message. Takes MessageID as a parameter
    """

    if request.json:
        for row in request.json:
            message = row.to_message()
            result = db.session.execute(
                '''
                DELETE FROM messages AS m
                WHERE id = :message_id
                '''
                , {message_id: message['MessageID']}
            )
        db.session.commit()
        return "Success: You deleted a message"




