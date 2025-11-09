import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import chainlit as cl
from tools.tool_registry import TOOLS, execute_function

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Enhanced system prompt for health & fitness
SYSTEM_PROMPT = """You are Elicia, an expert health and fitness AI coach with deep knowledge in:

- Exercise science and workout programming
- Nutrition and meal planning
- Body composition and metabolic calculations
- Strength training and progressive overload
- Cardiovascular fitness and endurance training
- Injury prevention and proper form

You have access to specialized tools for:
- Calculating BMI, TDEE, macros, body fat percentage, heart rate zones
- Generating personalized workout plans
- Creating meal plans and providing nutrition information
- Analyzing exercises and progressive overload strategies

**Important Guidelines:**
1. Always prioritize safety and encourage proper form
2. Recommend consulting healthcare professionals for medical concerns
3. Provide evidence-based advice
4. Be motivating and supportive
5. Ask clarifying questions when needed (age, weight, height, goals, etc.)
6. Use the available tools whenever calculations or structured plans are needed

**Disclaimer:** You are not a replacement for medical professionals. Always advise users to consult with doctors, especially before starting new exercise or diet programs.

Be friendly, encouraging, and knowledgeable. Help users achieve their health and fitness goals!
"""


@cl.on_chat_start
async def start():
    """Called when a new chat session starts."""
    # Initialize conversation history
    cl.user_session.set("messages", [{"role": "system", "content": SYSTEM_PROMPT}])

    await cl.Message(
        content="""👋 Welcome to **Elicia AI - Your Health & Fitness Coach!**

I'm here to help you with:

🏋️ **Fitness & Workouts**
- Personalized workout plans
- Exercise recommendations
- Progressive overload calculations

📊 **Body Metrics**
- BMI, TDEE, and macro calculations
- Body fat percentage estimates
- Heart rate training zones

🥗 **Nutrition**
- Meal planning
- Nutrition information
- Healthy food alternatives

💧 **Wellness**
- Hydration recommendations
- General health guidance

**Let's get started!** Tell me about your fitness goals, or ask me anything about health and fitness.

For example:
- "I'm 30, 180cm, 80kg. What's my BMI and daily calorie needs?"
- "Create a 4-day muscle building workout plan"
- "What are good protein sources and their nutrition?"
"""
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """
    Handle incoming messages from the user with function calling support.

    Args:
        message: The message object from Chainlit containing user input
    """
    # Get conversation history
    messages = cl.user_session.get("messages")

    # Add user message to history
    messages.append({"role": "user", "content": message.content})

    # Create a placeholder for the response
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Call OpenAI API with function calling
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # If the model wants to call functions
        if tool_calls:
            # Add assistant's response to messages
            messages.append(response_message)

            # Execute each function call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Show what tool is being used
                await msg.stream_token(f"\n\n🔧 Using tool: **{function_name}**\n\n")

                # Execute the function
                function_response = execute_function(function_name, function_args)

                # Add function response to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })

            # Get final response from the model with function results
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True
            )

            # Stream the final response
            for chunk in second_response:
                if chunk.choices[0].delta.content:
                    await msg.stream_token(chunk.choices[0].delta.content)

            # Update message history with assistant's final response
            final_content = msg.content
            messages.append({"role": "assistant", "content": final_content})
        else:
            # No function call, stream regular response
            messages.append({"role": "assistant", "content": response_message.content})
            await msg.stream_token(response_message.content)

        await msg.update()

        # Save updated conversation history
        cl.user_session.set("messages", messages)

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()


@cl.on_settings_update
async def setup_agent(settings):
    """Handle settings updates if needed."""
    pass
