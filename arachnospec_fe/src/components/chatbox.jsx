import { useState, useRef } from 'react';

export default function ChatBox({ onUserInput }) {
    const [messages, setMessages] = useState([]);
    const [isInputDisabled, setInputDisabled] = useState(false);
    const [isProcessingVideo, setIsProcessingVideo] = useState(true);
    const inputRef = useRef(null);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        const message = inputRef.current.value.trim();
        if (message === '') return;
        inputRef.current.value = ''; // Clear input after sending
        setMessages(oldMessages => [...oldMessages, { text: message, author: 'user' }]);
        setInputDisabled(true); // Disable input while processing response

        onUserInput?.(message);  // Optionally notify the parent component

        const endpoint = isProcessingVideo ? 'http://localhost:5000/process_video' : 'http://localhost:5000/chat';
        const payload = isProcessingVideo ? { url: message } : { message };

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        console.log(data);

        setMessages(oldMessages => [...oldMessages, { text: data.message || 'Error processing request', author: 'system' }]);
        setInputDisabled(false);
        if (isProcessingVideo) setIsProcessingVideo(false);  // Switch to chat mode after processing the URL
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex-grow overflow-auto p-4 bg-white shadow-inner">
                {messages.map((msg, index) => (
                    <div key={index} className={`text-left p-2 my-2 rounded ${msg.author === 'user' ? 'bg-blue-200' : 'bg-green-200'}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSendMessage} className="p-4">
                <input
                    type="text"
                    placeholder={isProcessingVideo ? "Enter YouTube URL here..." : "Type your message here..."}
                    className="border-2 p-2 w-full rounded"
                    ref={inputRef}
                    onChange={(e) => setInputDisabled(e.target.value.trim() === '')}
                    disabled={isInputDisabled}
                />
                <button type="submit" className="hidden">Send</button>
            </form>
        </div>
    );
}