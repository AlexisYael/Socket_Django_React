import logo from './logo.svg';
import './App.css';

function App(props) {
  props.ws.onopen = function () {
    props.ws.send(JSON.stringify({ message:"Hola karla", usuario:"juan" }))
  }

  props.ws.onmessage = function (msg) {
    console.log(JSON.parse(msg.data).message);
  } 
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
