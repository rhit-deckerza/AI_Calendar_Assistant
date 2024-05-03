import React, { useState } from 'react';
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";
import { fetchSystemPrompt } from './Utilities';

function Chat({ events, setEvents }) {  // Added events and setEvents as props
    const [messages, setMessages] = useState([]);
    const [openAIMessages, setOpenAIMessages] = useState([]);
    const [firstMessage, setFirstMessage] = useState(true);

    const appendCal = (messageText) => {
        let full_message = '<CAL>['
        events.forEach(function(element, index) {
            full_message += JSON.stringify(element, null, 2) + ", "
        }); 
        full_message += ']</CAL> ' + messageText
        return full_message
    }

    function extractCal(response) {
        // Regular expression to find text within <CAL> </CAL> tags
        const calRegex = /<CAL>(.*?)<\/CAL>/s;

        // Extract text within <CAL> </CAL>
        const match = response.match(calRegex);
        const textWithinTags = match ? match[1].trim() : '';

        // Remove text within <CAL> </CAL> tags, including the tags themselves
        const textWithoutTags = response.replace(calRegex, '').trim();

        // Initialize an array to hold the parsed JSON objects
        let jsonObjects = [];

        // Check if textWithinTags is not empty and parse it as JSON
        if (textWithinTags) {
            try {
                // Assuming the text within the tags is an array of JSON strings
                jsonObjects = JSON.parse(textWithinTags);
            } catch (error) {
                console.error('Error parsing JSON data:', error);
                // Handle the error or throw it depending on your error handling policy
            }
        }
        setEvents(jsonObjects)
        console.log(events)
        console.log(jsonObjects)
        
        return textWithoutTags
    }


    const handleSend = async (messageText) => {
        const newMessage = {
            message: messageText,
            sentTime: "just now",
            direction: "outgoing"
        };
        const message_with_calendar = appendCal(messageText)
        const newMessageOpenAI = { role: 'user', content: message_with_calendar };
        let toSend =  [...openAIMessages, newMessageOpenAI];
        if (firstMessage){
            const systemPrompt = await fetchSystemPrompt();
            const systemMessage = { role: 'system', content: systemPrompt };
            toSend = [...toSend, systemMessage];
            setFirstMessage(false);
        }

        await setMessages(currentMessages => [...currentMessages, newMessage]);

        const responsePromise = fetch("http://localhost:8080/api/prompt", {
            method: 'POST',
            body: JSON.stringify({
                messages: toSend
            }),
            headers: {
                'Content-Type': 'application/json'
            },
        });
        await setOpenAIMessages(toSend);

        responsePromise.then(async res => {
            if (res.status >= 400) {
                console.log(`Error when handling request: Code ${res.status}`);
            } else {
                const body = await res.json();

                const responseMessage = {
                    message: extractCal(body.response),
                    sentTime: "just now",
                    direction: "incoming"
                };
                const responseMessageOpenAI = { role: 'system', content: body.response };

                setMessages(currentMessages => [...currentMessages, responseMessage]);
                setOpenAIMessages(currentOpenAIMessages => [...currentOpenAIMessages, responseMessageOpenAI]);
                console.log(openAIMessages)
            }
        });
    };

    return (
        <div style={{ position: "relative", height: "500px" }}>
            <MainContainer>
                <ChatContainer>
                    <MessageList>
                        {messages.map((msg, index) => (
                            <Message
                                key={index}
                                model={{
                                    message: msg.message,
                                    direction: msg.direction
                                }}
                            />
                        ))}
                    </MessageList>
                    <MessageInput 
                        placeholder="Type message here" 
                        onSend={(_, text) => handleSend(text)} 
                        attachButton={false}
                    />
                </ChatContainer>
            </MainContainer>
        </div>
    );
}

export default Chat;
