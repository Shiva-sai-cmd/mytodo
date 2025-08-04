from flask_mail import Message
from flask import current_app
from extensions import mail

def send_email(to_email, username, is_todo=False, todo_title=None):
    try:
        if is_todo:
            subject = " New Todo Created!"
            body = f"Hi {username},\n\nYou just added a new todo: \"{todo_title}\".\nKeep being productive!"
        else:
            subject = " Welcome to MyTodoApp!"
            body = f"Hi {username},\n\nThank you for registering on MyTodoApp. Start organizing your day efficiently!"

        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[to_email]
        )
        msg.body = body
        mail.send(msg)
        print(" Email sent successfully!")
    except Exception as e:
        print(" Email sending failed:", str(e))
