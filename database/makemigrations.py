from database.connector import Base, engine

from app.models.document import Document
from app.models.conversation import ConversationModel
from app.models.messages import MessageModel

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()