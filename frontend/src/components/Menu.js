import React from "react";
import { BrowserRouter, Link } from 'react-router-dom';


function Menu(){
    const menuItems = [
        {label: 'Home', path: '/'},
        {label: 'Rent', path: '/rent'},
        {label: 'List', path: '/list'},
        {label: 'About', path: '/about'},
        {label: 'Contact', path: '/contact'},
    ];

    return (
        <nav className="menu">
            <ul>
                {menuItems.map((item) => (
                    <li key={item.label}>
                        <BrowserRouter>
                        <Link to={item.path}>{item.label}</Link>
                        </BrowserRouter>
                        
                    </li>
                ))}
            </ul>
        </nav>
    );
}
export default Menu;