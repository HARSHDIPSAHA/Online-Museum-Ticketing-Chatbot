import React from 'react';
import './Header.css'; // Import CSS for Header

function Header() {
  return (
    <header>
      <div className="logo">
        <img src="/logo-main.png" alt="NCSM Logo" />
      </div>
      <nav>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About Us</a></li>
          <li><a href="#activities">Activities</a></li>
          <li><a href="#gallery">Gallery</a></li>
          <li><a href="#contact">Contact Us</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
