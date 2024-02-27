// import Menu from './components/Menu';
import SearchBar from './components/Search';
import PropertyList from './components/Property';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignInUp from './components/SignInUp'; // import the SignInUp component
import Menu from './components/Menu';
import AboutUs from './components/AboutUs';
import ContactUs from './components/ContactUs'; // import the ContactUs component
import Footer from './components/Footer'; // import the Footer component
import PropertyPage from './components/PropertyPage'; // import the PropertyPage component


function App() {
  return (
    <div className="App">
       <h1 className='header'>RentEase App</h1>
       <SearchBar className="SearchBar" />
      <Router>
        <Menu className="Menu" />
        <Routes>
          <Route path="/signinup" element={<SignInUp className="SignInUp" />} />
          <Route path="/" element={<PropertyList className="PropertyList" />} />
          <Route path="/about" element={<AboutUs className="AboutUs" />} />
          <Route path="/contact" element={<ContactUs className="ContactUs" />} />
          <Route path="/properties/:propertyId" element={<PropertyPage />} />
        </Routes>
       
      </Router>
          <div className="footer">
              <Footer />
            </div>
    </div> 
  );
}

export default App;
