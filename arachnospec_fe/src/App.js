import { useState } from 'react';
import largeLogo from './assets/arachnospec_128.png';
import smallLogo from './assets/arachnospec_48.png';
import ChatBox from './components/chatbox';

function App() {
  const [isChatActive, setChatActive] = useState(false);

  const handleUserInput = () => {
    setChatActive(true); // This triggers when user starts typing
  };

  return (
    <div className="flex flex-col h-screen">
      <div className={`transition-all ease-in-out duration-500 ${isChatActive ? 'absolute top-4 right-4' : 'self-center mt-20'}`}>
        <img
          src={isChatActive ? smallLogo : largeLogo}
          alt="Logo"
          className={isChatActive ? 'w-12 h-12' : 'w-32 h-32'}
        />
      </div>
      <div className="flex-1 overflow-auto p-4">
        <ChatBox onUserInput={handleUserInput} />
      </div>
      <div className="p-4">
        {/* Additional UI components or footer could go here */}
      </div>
    </div>
  );

}

export default App;
