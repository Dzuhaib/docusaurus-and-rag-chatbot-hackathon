import React, { useState, useRef, useEffect, useCallback } from 'react';
import styles from './Chatbot.module.css';

const ChatIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
    <path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18z"/>
  </svg>
);

const CloseIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
  </svg>
);

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [selectedTextContext, setSelectedTextContext] = useState(null);
  const [feedbackSent, setFeedbackSent] = useState({});

  const BOT_NAME = 'Book Assistant'; // Changed chatbot title
  const USER_NAME = 'You';

  useEffect(() => {
    const handleTextSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedTextContext(selectedText);
        setIsOpen(true);
      }
    };
    document.addEventListener('mouseup', handleTextSelection);
    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userQueryForFeedback = input; 
    const currentContextForFeedback = selectedTextContext;

    const userMessage = { sender: USER_NAME, text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    let streamingMessageId = null; // Declare with let outside try
    let initialBotMessage = null;   // Declare with let outside try

    try {
      // Prepare conversation history: last N messages, excluding the current user message
      const conversationHistory = messages.slice(-4).map(msg => ({
        sender: msg.sender,
        text: msg.text,
      }));

      streamingMessageId = `temp-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`; // Assign value
      initialBotMessage = { // Assign value
        sender: BOT_NAME,
        text: '',
        sources: [],
        message_id: streamingMessageId,
        userQuery: userQueryForFeedback,
        contextUsed: currentContextForFeedback,
        isStreaming: true, // Flag to indicate it's a streaming message
      };
      setMessages((prevMessages) => [...prevMessages, initialBotMessage]);


      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Stream-Response': 'true', // Indicate that we want a streaming response
        },
        body: JSON.stringify({
          query: userQueryForFeedback, 
          context: currentContextForFeedback,
          history: conversationHistory,
        }),
      });

      if (!response.ok) {
        // Handle non-streaming errors (e.g., HTTP 500 without a body to stream)
        const errorData = await response.json(); // Try to parse error message
        throw new Error(`HTTP error! status: ${response.status} - ${errorData.detail || response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      let finalBotMessage = { ...initialBotMessage, isStreaming: false }; // Prepare final message structure

      const updateStreamingMessage = (updateFn) => {
        setMessages(prevMessages => 
          prevMessages.map(msg => 
            msg.message_id === streamingMessageId ? { ...msg, ...updateFn(msg) } : msg
          )
        );
      };

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split('\n');
        buffer = parts.pop(); // Keep incomplete part in buffer

        for (const part of parts) {
          if (!part) continue;
          try {
            const chunk = JSON.parse(part);
            if (chunk.type === 'sources') {
              finalBotMessage.sources = chunk.content;
              updateStreamingMessage(msg => ({ sources: chunk.content }));
            } else if (chunk.type === 'chunk') {
              finalBotMessage.text += chunk.content;
              updateStreamingMessage(msg => ({ text: msg.text + chunk.content }));
            } else if (chunk.type === 'error') {
              finalBotMessage.text += `Error: ${chunk.content}`;
              updateStreamingMessage(msg => ({ text: msg.text + `Error: ${chunk.content}` }));
              throw new Error(chunk.content); // Re-throw to exit stream and show error
            }
          } catch (e) {
            console.error('Error parsing chunk:', e, 'Part:', part);
            updateStreamingMessage(msg => ({ text: msg.text + `\n[Stream Error: ${e.message}]` }));
            break; 
          }
        }
      }
      
      updateStreamingMessage(msg => ({ isStreaming: false, text: finalBotMessage.text, sources: finalBotMessage.sources }));

    } catch (error) {
      console.error('Error sending message:', error);
      // Fallback if initial fetch fails or stream errors out
      // Only remove the streaming message if it was successfully added
      if (streamingMessageId) {
        setMessages((prevMessages) => [
          ...prevMessages.filter(msg => msg.message_id !== streamingMessageId), 
          { sender: BOT_NAME, text: `Error: ${error.message}. Please try again.` },
        ]);
      } else {
        setMessages((prevMessages) => [
          ...prevMessages, 
          { sender: BOT_NAME, text: `Error: ${error.message}. Please try again.` },
        ]);
      }
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) handleSendMessage();
  };

  const toggleChat = useCallback(() => {
    setIsOpen(prev => !prev);
    if (isOpen) {
      setSelectedTextContext(null);
      setMessages([]);
      setFeedbackSent({}); // Clear feedback status when chat is closed
    }
  }, [isOpen]);

  const handleFeedback = async (messageId, rating) => {
    const messageToRate = messages.find(msg => msg.message_id === messageId);

    if (!messageToRate) {
      console.error("Message not found for feedback:", messageId);
      return;
    }

    try {
      await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_id: messageToRate.message_id,
          query: messageToRate.userQuery,
          response: messageToRate.text,
          sources: messageToRate.sources,
          rating: rating,
          context: messageToRate.contextUsed,
        }),
      });
      setFeedbackSent(prev => ({ ...prev, [messageId]: true }));
      console.log(`Feedback ${rating} sent for message ${messageId}`);
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
  };

  return (
    <>
      {!isOpen && (
        <button className={styles.chatToggleButton} onClick={toggleChat} aria-label="Open chat">
          <ChatIcon />
        </button>
      )}

      {isOpen && (
        <div className={styles.chatbotContainer}>
          <div className={styles.chatbotHeader}>
            <h3>{BOT_NAME}</h3>
            <button className={styles.closeButton} onClick={toggleChat} aria-label="Close chat">
              <CloseIcon />
            </button>
          </div>
          <div className={styles.messagesContainer}>
            {selectedTextContext && (
              <div className={styles.contextInfo}>
                <p>Asking about:</p>
                <blockquote>{selectedTextContext}</blockquote>
              </div>
            )}
            {messages.length === 0 && !selectedTextContext && (
              <div className={styles.welcomeMessage}>
                Welcome! Ask me anything about the book, or select text on the page to ask about it.
              </div>
            )}
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`${styles.message} ${ 
                  msg.sender === USER_NAME ? styles.userMessage : styles.botMessage
                }`}
              >
                <span className={styles.sender}>{msg.sender}:</span> {msg.text}
                {msg.sender === BOT_NAME && msg.message_id && !feedbackSent[msg.message_id] && (
                  <div className={styles.feedbackButtons}>
                    <button onClick={() => handleFeedback(msg.message_id, 'good')} title="Good response">👍</button>
                    <button onClick={() => handleFeedback(msg.message_id, 'bad')} title="Bad response">👎</button>
                  </div>
                )}
                {/* Render sources if they exist */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sourcesContainer}>
                    <strong>Sources:</strong>
                    <ul>
                      {msg.sources.map((source, idx) => (
                        <li key={idx}>
                          <a href={source.url} target="_blank" rel="noopener noreferrer">
                            {source.page_title}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className={styles.loadingMessage}>
                <span className={styles.sender}>{BOT_NAME}:</span> Thinking...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className={styles.inputContainer}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the book or selected text..."
              className={styles.inputField}
              disabled={isLoading}
            />
            <button onClick={handleSendMessage} className={styles.sendButton} disabled={isLoading}>
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default Chatbot;