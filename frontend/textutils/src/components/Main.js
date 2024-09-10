import React from 'react';
import './Main.css'; // Import CSS for Main

function Main() {
  return (
    <main>
      <section id="about">
        <h2>Who We Are</h2>
        <p>NCSM, an autonomous society under the Ministry of Culture, was formed in 1978...</p>
      </section>
      
      <section id="activities">
        <h2>Activities</h2>
        <ul>
          <li>Mobile Science Exhibitions</li>
          <li>Lectures and Demonstrations</li>
          <li>Training and Workshops</li>
        </ul>
      </section>
      
      <section id="gallery">
        <h2>Gallery</h2>
        <p>Check out our Virtual Gallery and Video Gallery showcasing different events and exhibits.</p>
      </section>
    </main>
  );
}

export default Main;
