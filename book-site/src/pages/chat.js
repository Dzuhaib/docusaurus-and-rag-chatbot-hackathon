import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot';

function ChatPage() {
  return (
    <Layout title="Chat with AI" description="Chat with our AI assistant powered by RAG">
      <main>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '20px' }}>
          <Chatbot />
        </div>
      </main>
    </Layout>
  );
}

export default ChatPage;
