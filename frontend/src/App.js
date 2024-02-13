import Menu from './components/Menu';
import SearchBar from './components/Search';
import PropertyList from './components/Property';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className='background'>
       <h1 className='header'>RentEase App</h1>
      <SearchBar />
      <Menu />
      </div>
      <PropertyList />
    
    </div>
  );
}

export default App;
