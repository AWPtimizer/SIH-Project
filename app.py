from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

# Initialize an empty list to store the chat history
chat_history = []

# Function to interact with AyurBot
def chat_with_ayurbot(user_message):
    # Send a message to AyurBot using GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are chatting with AyurBot, your quirky Ayurvedic buddy."},
            {"role": "user", "content": user_message},
        ],
        max_tokens=500,  # Adjust the response length as needed
        api_key=openai.api_key,
    )

    # Extract and return AyurBot's reply
    return response['choices'][0]['message']['content']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_input']

    # Append user message to the chat history
    chat_history.append({"role": "user", "content": user_message})

    # Call the chat_with_ayurbot function to get AyurBot's response
    bot_response = chat_with_ayurbot(user_message).split('\n')  # Split responses by newlines
    # bot_response = [{"role": "bot", "content": response} for response in bot_response]

    # Append bot responses to the chat history
    for response in bot_response:
        chat_history.append({"role": "bot", "content": response})

    # Pass the chat history to the template
    return render_template('chat.html', chat_history=chat_history)


if __name__ == '__main__':
    app.run(debug=True)
