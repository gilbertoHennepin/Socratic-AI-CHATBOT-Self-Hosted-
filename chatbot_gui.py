# split the terminal and run 
# python chatbot_gui.py

import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QScrollArea, QLabel, QFrame
)

API_URL = "http://127.0.0.1:5000/chat"

# ---------- Bubble Widget ----------
class MessageBubble(QWidget):
    def __init__(self, text, is_user=False):
        super().__init__()
        layout = QHBoxLayout()

        label = QLabel(text)
        label.setWordWrap(True)
        label.setMaximumWidth(400)

        if is_user:
            layout.addStretch()
            layout.addWidget(label)
            label.setStyleSheet("background-color: #2e86de; color: white; padding: 8px; border-radius: 10px;")
        else:
            layout.addWidget(label)
            layout.addStretch()
            label.setStyleSheet("background-color: #444; color: white; padding: 8px; border-radius: 10px;")

        self.setLayout(layout)

# ---------- Main Chat Window ----------
class ChatbotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Socratic Tutor Chatbot")
        self.resize(600, 500)

        self.layout = QVBoxLayout(self)

        # Scrollable chat area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.addStretch()
        self.scroll.setWidget(self.chat_content)

        self.layout.addWidget(self.scroll)

        # Input area
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)
        self.layout.addLayout(input_layout)

    def send_message(self):
        user_message = self.input_box.text().strip()
        if not user_message:
            return
        self.input_box.clear()

        # Add user bubble
        self.chat_layout.insertWidget(self.chat_layout.count()-1, MessageBubble(user_message, is_user=True))

        try:
            response = requests.post(API_URL, json={"message": user_message})
            bot_reply = response.json().get("reply", "Error: No reply")
        except Exception as e:
            bot_reply = f"Error: {e}"

        # Add bot bubble
        self.chat_layout.insertWidget(self.chat_layout.count()-1, MessageBubble(bot_reply, is_user=False))

        # Auto-scroll
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

# ---------- Run App ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotUI()
    window.show()
    sys.exit(app.exec())
