import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("Missing GITHUB_TOKEN")

# Setup OpenAI async client (adjust base_url and model if you're using Azure or another hosted inference)
client = AsyncOpenAI(
    api_key=GITHUB_TOKEN,
    base_url="https://models.inference.ai.azure.com/"
)
chat_service = OpenAIChatCompletion(
    ai_model_id="gpt-4o-mini",
    async_client=client
)

# Define the Travel Agent AI with helpful instructions
agent = ChatCompletionAgent(
    service=chat_service,
    name="TravelAgent",
    instructions="""
You are TravelAgent, an AI assistant that helps users plan vacations and trips based on their interests.

Your responsibilities:
- Greet the user at the beginning of the conversation.
- Ask what kind of trip they are looking for (destination, activities, length of stay, etc).
- Always plan trips based on user-specified locations and preferences.
- If the user doesn’t specify a destination, ask clarifying questions to guide them.
- Provide well-structured plans including key places to visit, activities to try, and tips for travel.
- Be proactive but never pushy — do not suggest random destinations unless explicitly asked.

Initial greeting (only at the start of the conversation):
"Hello! I'm your TravelAgent assistant. I can help you plan the perfect vacation! Here's what I can do:
1. Plan a day trip to a specific location
2. Create full travel itineraries
3. Recommend things to do based on your interests
4. Help with logistics like duration and season

Where would you like to go, or what kind of trip are you thinking about today?"
"""
)

# Main async loop to run the conversation
async def main():
    thread: ChatHistoryAgentThread = None

    while True:
        print("\n# 🤖 TravelAgent: Where would you like to travel or what kind of vacation are you thinking of? (type 'exit' to quit)")

        user_input = input("# 👤 User: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye! Safe travels! ✈️")
            break

        first_chunk = True
        try:
            # Stream the AI's response
            async for response in agent.invoke_stream(messages=user_input, thread=thread):
                if first_chunk:
                    print(f"# 🤖 {response.name}: ", end="", flush=True)
                    first_chunk = False
                print(response, end="", flush=True)
                thread = response.thread
            print()
        except Exception as e:
            print(f"\n❌ Error: {e}")

    if thread:
        await thread.delete()

# Run the main function
asyncio.run(main())