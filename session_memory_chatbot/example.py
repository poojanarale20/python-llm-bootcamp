#!/usr/bin/env python3
"""
Stateful Chatbot with Memory - Demo Script
This script demonstrates the key features of the stateful chatbot.
"""

from chatbot import StatefulChatbot
import time

def demo_chatbot():
    """Demonstrate the stateful chatbot features."""
    print("🤖 Stateful Chatbot Demo")
    print("=" * 50)
    
    try:
        # Initialize chatbot
        print("Initializing chatbot...")
        chatbot = StatefulChatbot()
        print("✅ Chatbot initialized successfully!")
        
        # Start a session
        session_id = "demo_user_123"
        user_name = "Alice"
        
        print(f"\n🚀 Starting session for {user_name} (ID: {session_id})")
        welcome = chatbot.start_session(session_id, user_name)
        print(f"Bot: {welcome}")
        
        # Set some user preferences
        print("\n📝 Setting user preferences...")
        chatbot.update_user_preference(session_id, "favorite_color", "blue")
        chatbot.update_user_preference(session_id, "programming_language", "Python")
        chatbot.update_user_preference(session_id, "hobby", "reading")
        print("✅ Preferences set!")
        
        # Demo conversation
        demo_messages = [
            "Hello! What's my name?",
            "What's my favorite color?",
            "I love programming in Python. Can you help me with a simple function?",
            "Can you write a function to calculate fibonacci numbers?",
            "That's great! Now, what do you remember about my hobbies?",
            "I'm also interested in machine learning. Can you recommend some resources?",
            "What programming language should I focus on for ML?",
            "Thanks for the advice! Can you summarize what we've talked about so far?",
            "I want to set a new preference - my favorite ML framework is TensorFlow",
            "Perfect! Now what's my updated profile?",
            "This is a test message to see memory management",
            "And another message for testing",
            "One more message to test conversation summarization",
            "Final test message - let's see if conversation gets summarized now!"
        ]
        
        print("\n💬 Demo Conversation:")
        print("-" * 30)
        
        for i, message in enumerate(demo_messages, 1):
            print(f"\n[{i}] You: {message}")
            
            # Add some delay to make it more realistic
            time.sleep(0.5)
            
            response = chatbot.chat(message, session_id)
            print(f"Bot: {response}")
            
            # Show session info every few messages
            if i % 5 == 0:
                session_info = chatbot.get_session_info(session_id)
                print(f"\n📊 Session Info - Messages: {session_info['message_count']}, "
                      f"Buffer Size: {session_info['memory_buffer_size']}")
        
        # Show final profile and history
        print("\n" + "=" * 50)
        print("📋 Final User Profile:")
        profile = chatbot.get_user_profile(session_id)
        if profile:
            print(f"  Name: {profile['name']}")
            print(f"  Preferences: {profile['preferences']}")
            print(f"  Total Messages: {len(profile['conversation_history'])}")
        
        print("\n📜 Recent Conversation History:")
        history = chatbot.get_conversation_history(session_id)
        if history:
            # Show last 3 messages
            recent = history[-3:] if len(history) >= 3 else history
            for i, msg in enumerate(recent, 1):
                print(f"  {i}. You: {msg['user']}")
                print(f"     Bot: {msg['assistant'][:100]}{'...' if len(msg['assistant']) > 100 else ''}")
        
        # Test memory clearing
        print("\n🧹 Testing memory clearing...")
        chatbot.clear_memory(session_id)
        print("✅ Memory cleared!")
        
        # Test if memory is actually cleared
        test_response = chatbot.chat("Do you remember my name?", session_id)
        print(f"\nTest after clearing memory:")
        print(f"You: Do you remember my name?")
        print(f"Bot: {test_response}")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\nMake sure to:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your OpenAI API key in a .env file")
        print("3. Copy env_example.txt to .env and add your API key")

def demo_features():
    """Demonstrate specific features."""
    print("\n🔧 Feature Demonstrations:")
    print("=" * 30)
    
    try:
        chatbot = StatefulChatbot()
        session_id = "feature_test"
        
        # Test session management
        print("1. Session Management:")
        chatbot.start_session(session_id, "TestUser")
        chatbot.update_user_preference(session_id, "test_pref", "test_value")
        profile = chatbot.get_user_profile(session_id)
        print(f"   ✅ Profile created: {profile['name']}")
        
        # Test conversation
        print("2. Conversation with Memory:")
        response1 = chatbot.chat("My name is TestUser", session_id)
        response2 = chatbot.chat("What's my name?", session_id)
        print(f"   ✅ Memory working: {response2}")
        
        # Test preferences
        print("3. User Preferences:")
        response3 = chatbot.chat("What's my test_pref value?", session_id)
        print(f"   ✅ Preferences working: {response3}")
        
        # Test session info
        print("4. Session Information:")
        info = chatbot.get_session_info(session_id)
        print(f"   ✅ Session info: {info}")
        
        print("\n✅ All features working correctly!")
        
    except Exception as e:
        print(f"❌ Feature test failed: {e}")

if __name__ == "__main__":
    # Run the main demo
    demo_chatbot()
    
    # Run feature tests
    demo_features()
