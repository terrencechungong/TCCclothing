import React, {useState} from 'react';
import logo from './logo.svg';
import './App.css';
import Login from './components/Login';
import Register from './components/Register';
import { MapContainer } from './components/LoginPage';


function App() {
  const [currentForm, SetCurrentForm] = useState('login');
  const toggleForm = (formName:string) => {
    SetCurrentForm(formName)
  }
  return (
    <MapContainer/>
  );
}


export default App;
