import React, { useState, useEffect, useMemo } from 'react';
import { BrowserRouter, Route,Routes, NavLink,useLocation } from 'react-router-dom';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sign from '../src/components/Signup.js';
import Signin from '../src/components/Signin.js';
import About from '../src/components/About.js';
import Home from '../src/components/Home.js';
import Journal from '../src/components/journal.js';
import Database from '../src/components/db.js';
import Settings from '../src/components/settings.js';
import Privacy from '../src/components/Privacy.js';
import Profile from '../src/components/Profile.js';
import Editprofile from '../src/components/editprof.js';
import Test from '../src/components/Test.js';
import logo from '../src/assets/logo.png';


function Navbar() {
  const location = useLocation();
  const masquerNavbarSurPages = useMemo(() => ['/Profile','/journal','/database','/notification','/settings','/privacy-settings','/editprofile','/test'], []);
  
  const [afficherNavbar, setAfficherNavbar] = useState(true);

  useEffect(() => {
    const masquerNavbar = masquerNavbarSurPages.includes(location.pathname);
    setAfficherNavbar(!masquerNavbar);
  }, [location.pathname, masquerNavbarSurPages]);

  return (
    <div className='navlinks'>
      {afficherNavbar && (
        <>
          <img src={logo} alt="Logo" className='logo' />
         
          <NavLink className='button' activeclassname="active" to="/Sign-Up">Sign Up</NavLink>
          <NavLink className='button' activeclassname="active" to="/Sign-In">Sign In</NavLink>
          <NavLink className='button1' activeclassname="active" to="/about">About</NavLink>

          {/* Horizontal line to separate the navbar from the rest of the content */}
          <hr className="navbar-separator" />
        </>
      )}
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/Sign-Up' element={<Sign />} />
        <Route path="/Sign-In" element={<Signin />} />
        <Route path="/about" element={<About />} />
        <Route path="/journal" element={<Journal />} />
        <Route path="/database" element={<Database />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/privacy-settings" element={<Privacy />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/editprofile" element={<Editprofile />} />
        <Route path='/test' element={<Test />} />
      </Routes>
    </div>
  );
}


function App() {
  return (
    <BrowserRouter>
      <Navbar />
    </BrowserRouter>
  );
}

export default App;
