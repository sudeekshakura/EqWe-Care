import logo from './logo.svg';
import './App.css';
import Header from './header';
import Chatbot from './conversational';
function App() {
  return (
    <div className="App">
      <Header/>
      <header className="App-header">
        <Chatbot/>
      </header>
    </div>
  );
}

export default App;
