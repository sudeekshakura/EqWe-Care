import React from 'react';
import Search from './search';
import img1 from './logo.png'
function Header() {
  return (
    <div>
    <header style={styles.header}>
    <img style={{width:"100px"}}src={img1}></img>

      <div style={styles.logo}>
        <h1 style={styles.logoText}>EqWe Care</h1>
      </div>
      <nav style={styles.nav}>
        <a href="#" style={styles.navLink}>Home</a>
        <a href="#" style={styles.navLink}>Services</a>
        <a href="#" style={styles.navLink}>Doctors</a>
        <a href="#" style={styles.navLink}>Contact</a>
      </nav>
    </header>
    <div><Search/></div>
    </div>
  );
}

const styles = {
  header: {
    backgroundColor: '#1976d2', // Blue color (you can adjust as needed)
    padding: '5px 5px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
  },
 
  logoImg: {
    width: '50px', // Adjust size as needed
    marginRight: '10px',
  },
  logoText: {
    color: '#fff', // White color for text
    fontFamily: 'Arial, sans-serif', // Adjust font family as needed
    marginLeft:'200px',
  },
  nav: {
    display: 'flex',
    marginRight:"100px"
  },
  navLink: {
    color: '#fff', // White color for links
    fontFamily: 'Arial, sans-serif', // Adjust font family as needed
    textDecoration: 'none',
    margin: '0 10px',
  },
};

export default Header;
