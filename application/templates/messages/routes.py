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
        , {chat_id: ChatID, user_id: UserID })
    db.session.commit()
    return jsonify(result.to_message())


@MessageAPI.route('/api/chats/<ChatID>/messages?UserID=<UserID>', methods=['POST'])
def send_message():
    """
    Allows a user to send a message. Takes as arguments GroupID, SenderID and Content
    """
    #
    if request.json: # If there is data in the POST request
        data = request.json.to_message()

        result = db.session.execute(
            '''
            INSERT INTO 
              messages AS m (m.GroupID, m.SenderID, m.content) 
            VALUES 
              (:chat_id, :sender_id, :content)
            '''
        ,{chat_id: data['ChatID'], sender_id: data['SenderID'], content: data['content']})
    return "Created new message "


