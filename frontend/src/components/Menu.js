import React from "react";
import { Link } from 'react-router-dom';
import '../index.css'



function Menu(){
    const menuItems = [
        {label: 'Home', path: '/'},
        {label: 'Rent', path: '/rent'},
        {label: 'About', path: '/about'},
        {label: 'Contact', path: '/contact'},
        {label: 'Sign In/Up', path: "/signinup"},
    ];

    return (
        <nav className="menu">
            <ul >
                {menuItems.map((item) => (
                    <li key={item.label}>
                        <Link to={item.path}>{item.label}</Link> 
                    </li>
                ))}
            </ul>
        </nav>
    );
}
export default Menu;
