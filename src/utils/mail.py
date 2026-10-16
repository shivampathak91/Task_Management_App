from fastapi_mail import FastMail,MessageSchema,ConnectionConfig,MessageType
from pydantic import EmailStr,BaseModel
from typing import List



conf = ConnectionConfig(
    MAIL_USERNAME = "@gmail.com",
    MAIL_PASSWORD = "your app password",
    MAIL_FROM = "@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Shivam Learnings",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(email: List[str]):
    html = """<p>Hi, Thanks for Registration. Our Team will connect you soon.</p> """

    message = MessageSchema(
        subject="Registartion Confirmation",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}