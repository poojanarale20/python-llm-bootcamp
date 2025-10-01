"""
Stateful Chatbot with Memory
A Python chatbot implementation that maintains conversation memory and user profiles 
using OpenAI's API and LangChain.
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.schema import BaseMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain

# Load environment variables
load_dotenv()

class StatefulChatbot:
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the stateful chatbot with memory capabilities."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.base_url = base_url or os.getenv("BASE_URL")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model_name=self.model_name,
            base_url=self.base_url,
            temperature=0.7
        )
        
        # Initialize memory stores
        self.session_memory = ConversationBufferWindowMemory(
            k=10,  # Keep last 10 messages in buffer
            return_messages=True
        )
        
        # Summary memory for long conversations
        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm,
            return_messages=True
        )
        
        # User profile storage
        self.user_profiles: Dict[str, Dict] = {}
        
        # Current conversation state
        self.current_session_id: Optional[str] = None
        self.message_count = 0
        
        # Create conversation chain
        self._setup_conversation_chain()
    
    def _setup_conversation_chain(self):
        """Setup the conversation chain with memory."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant with memory capabilities. 
            You remember previous conversations and can access user profile information.
            Be friendly, helpful, and maintain context across conversations.
            
            When you have access to user profile information (name, preferences), 
            use it to personalize your responses appropriately."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.session_memory,
            prompt=prompt,
            verbose=False
        )
    
    def start_session(self, session_id: str, user_name: Optional[str] = None) -> str:
        """Start a new conversation session."""
        self.current_session_id = session_id
        self.message_count = 0
        
        # Initialize user profile if name provided
        if user_name:
            if session_id not in self.user_profiles:
                self.user_profiles[session_id] = {
                    "name": user_name,
                    "preferences": {},
                    "conversation_history": []
                }
            else:
                self.user_profiles[session_id]["name"] = user_name
        
        return f"Session {session_id} started. Hello{' ' + user_name if user_name else ''}!"
    
    def get_user_profile(self, session_id: str) -> Optional[Dict]:
        """Retrieve user profile information."""
        return self.user_profiles.get(session_id)
    
    def update_user_preference(self, session_id: str, key: str, value: str):
        """Update user preference."""
        if session_id not in self.user_profiles:
            self.user_profiles[session_id] = {"name": None, "preferences": {}, "conversation_history": []}
        
        self.user_profiles[session_id]["preferences"][key] = value
    
    def _should_summarize(self) -> bool:
        """Check if conversation should be summarized (more than 10 messages)."""
        return self.message_count > 10
    
    def _summarize_conversation(self):
        """Summarize the current conversation and move to summary memory."""
        if self.message_count > 10:
            # Get current conversation history
            history = self.session_memory.chat_memory.messages
            
            # Create summary
            conversation_text = "\n".join([f"{'Human' if i % 2 == 0 else 'Assistant'}: {msg.content}" 
                                         for i, msg in enumerate(history)])
            
            summary_prompt = f"""
            Please summarize the following conversation in 2-3 sentences, 
            focusing on key topics, decisions, and important information:
            
            {conversation_text}
            """
            
            summary = self.llm.invoke(summary_prompt).content
            
            # Clear session memory and add summary to summary memory
            self.session_memory.clear()
            self.summary_memory.save_context(
                {"input": "Conversation Summary"},
                {"output": summary}
            )
            
            # Reset message count
            self.message_count = 0
            
            return summary
        return None
    
    def chat(self, message: str, session_id: Optional[str] = None) -> str:
        """Process a chat message and return response."""
        if session_id and session_id != self.current_session_id:
            self.start_session(session_id)
        
        if not self.current_session_id:
            raise ValueError("No active session. Please start a session first.")
        
        # Increment message count
        self.message_count += 1
        
        # Check if we need to summarize
        if self._should_summarize():
            summary = self._summarize_conversation()
            if summary:
                print(f"[System] Conversation summarized: {summary}")
        
        # Get user profile context
        profile_context = ""
        if self.current_session_id in self.user_profiles:
            profile = self.user_profiles[self.current_session_id]
            if profile["name"]:
                profile_context += f"User's name: {profile['name']}. "
            if profile["preferences"]:
                prefs = ", ".join([f"{k}: {v}" for k, v in profile["preferences"].items()])
                profile_context += f"User preferences: {prefs}. "
        
        # Add profile context to message
        enhanced_message = f"{profile_context}{message}" if profile_context else message
        
        # Get response from conversation chain
        response = self.conversation.predict(input=enhanced_message)
        
        # Store conversation in user profile
        if self.current_session_id in self.user_profiles:
            self.user_profiles[self.current_session_id]["conversation_history"].append({
                "user": message,
                "assistant": response
            })
        
        return response
    
    def get_conversation_history(self, session_id: Optional[str] = None) -> List[Dict]:
        """Get conversation history for a session."""
        target_session = session_id or self.current_session_id
        if target_session and target_session in self.user_profiles:
            return self.user_profiles[target_session]["conversation_history"]
        return []
    
    def clear_memory(self, session_id: Optional[str] = None):
        """Clear memory for a session."""
        target_session = session_id or self.current_session_id
        if target_session:
            self.session_memory.clear()
            self.summary_memory.clear()
            if target_session in self.user_profiles:
                self.user_profiles[target_session]["conversation_history"] = []
            self.message_count = 0
    
    def get_session_info(self, session_id: Optional[str] = None) -> Dict:
        """Get information about the current or specified session."""
        target_session = session_id or self.current_session_id
        if not target_session:
            return {"error": "No active session"}
        
        profile = self.user_profiles.get(target_session, {})
        return {
            "session_id": target_session,
            "message_count": self.message_count,
            "user_name": profile.get("name"),
            "preferences": profile.get("preferences", {}),
            "history_length": len(profile.get("conversation_history", [])),
            "memory_buffer_size": len(self.session_memory.chat_memory.messages)
        }
