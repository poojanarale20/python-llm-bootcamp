#!/usr/bin/env python3
"""
Stateful Chatbot with Memory - CLI Interface
"""

import sys
from chatbot import StatefulChatbot

def main():
    """Main CLI interface for the stateful chatbot."""
    print("🤖 Stateful Chatbot with Memory")
    print("=" * 40)
    
    try:
        # Initialize chatbot
        chatbot = StatefulChatbot()
        print("✅ Chatbot initialized successfully!")
        
        # Get session info
        session_id = input("Enter session ID (or press Enter for 'default'): ").strip() or "default"
        user_name = input("Enter your name (optional): ").strip() or None
        
        # Start session
        welcome_msg = chatbot.start_session(session_id, user_name)
        print(f"\n{welcome_msg}")
        print("\nCommands:")
        print("  /profile - Show user profile")
        print("  /history - Show conversation history")
        print("  /info - Show session information")
        print("  /pref <key> <value> - Set user preference")
        print("  /clear - Clear memory")
        print("  /quit - Exit chatbot")
        print("\nStart chatting! (Type your message and press Enter)")
        print("-" * 40)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == "/quit":
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == "/profile":
                    profile = chatbot.get_user_profile(session_id)
                    if profile:
                        print(f"\n📋 User Profile:")
                        print(f"  Name: {profile.get('name', 'Not set')}")
                        print(f"  Preferences: {profile.get('preferences', {})}")
                        print(f"  Messages in history: {len(profile.get('conversation_history', []))}")
                    else:
                        print("No profile found for this session.")
                    continue
                elif user_input.lower() == "/history":
                    history = chatbot.get_conversation_history(session_id)
                    if history:
                        print(f"\n📜 Conversation History ({len(history)} messages):")
                        # Show last 5 messages
                        recent_history = history[-5:] if len(history) > 5 else history
                        for i, msg in enumerate(recent_history, 1):
                            print(f"  {i}. You: {msg['user']}")
                            print(f"     Bot: {msg['assistant'][:100]}{'...' if len(msg['assistant']) > 100 else ''}")
                    else:
                        print("No conversation history found.")
                    continue
                elif user_input.lower() == "/info":
                    session_info = chatbot.get_session_info(session_id)
                    print(f"\n📊 Session Information:")
                    print(f"  Session ID: {session_info.get('session_id', 'N/A')}")
                    print(f"  Message Count: {session_info.get('message_count', 0)}")
                    print(f"  User Name: {session_info.get('user_name', 'Not set')}")
                    print(f"  Preferences: {session_info.get('preferences', {})}")
                    print(f"  History Length: {session_info.get('history_length', 0)}")
                    print(f"  Memory Buffer Size: {session_info.get('memory_buffer_size', 0)}")
                    continue
                elif user_input.lower() == "/clear":
                    chatbot.clear_memory(session_id)
                    print("🧹 Memory cleared!")
                    continue
                elif user_input.startswith("/pref "):
                    parts = user_input.split(" ", 2)
                    if len(parts) >= 3:
                        key, value = parts[1], parts[2]
                        chatbot.update_user_preference(session_id, key, value)
                        print(f"✅ Preference set: {key} = {value}")
                    else:
                        print("Usage: /pref <key> <value>")
                    continue
                
                # Process regular message
                response = chatbot.chat(user_input, session_id)
                print(f"\nBot: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        print("\nMake sure to:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your OpenAI API key in a .env file or environment variable")
        print("3. Copy env_example.txt to .env and add your API key")
        sys.exit(1)

if __name__ == "__main__":
    main()
