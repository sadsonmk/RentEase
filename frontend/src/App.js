import Menu from './components/Menu';
import SearchBar from './components/Search';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className='background'>
       <h1 className='header'>RentEase App</h1>
      <SearchBar />
      <Menu />
      </div>
    
    </div>
  );
}

export default App;
