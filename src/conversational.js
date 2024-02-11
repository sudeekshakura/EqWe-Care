import React, { useState } from 'react';
import { FaCommentAlt } from 'react-icons/fa';
import './Chatbot.css'; // Import your CSS file for styling

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const closeChatbot = () => {
    setIsOpen(false);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    const userInput = e.target.elements.message.value;
    e.target.elements.message.value = "";
    const newMessage = { text: userInput, type: 'user' };
    if (userInput.trim() === '') return;
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({'user_inp':userInput})
  };
    setMessages([...messages, newMessage]);
    // Here you can implement logic to handle the user's input and generate bot responses
    // For demonstration, I'm just sending a dummy bot response after a short delay
    fetch('http://localhost:5000/get_bot_response', requestOptions)
    .then((response) => response.json())
    .then((res) => {
      const botResponse = { text: res['response'], type: 'traversaal bot' };
    setMessages([...messages, newMessage, botResponse]);
    });
    }

  return (
    <div className="chatbot-container">
      {!isOpen && (
        <div className="chatbot-icon" onClick={toggleChatbot}>
          <FaCommentAlt size={30} />
        </div>
      )}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-title">TraverSaal Bot</div>
            <button className="close-button" onClick={closeChatbot}>
              <span>&times;</span>
            </button>
          </div>
          <div className="chatbot-messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.type}`} style={{textAlign:"left",fontSize:"10px"}}>
                {message.text}
              </div>
            ))}
          </div>
          <form className="message-form" onSubmit={handleSendMessage}>
            <input type="text" name="message" placeholder="Type your message..." />
            <button type="submit">Send</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
