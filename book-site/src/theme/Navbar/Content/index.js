import React, { useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import OriginalNavbarContent from '@theme-original/Navbar/Content';
import netlifyIdentity from 'netlify-identity-widget';
import styles from './index.module.css';

export default function NavbarContent(props) {
  const [user, setUser] = useState(netlifyIdentity.currentUser());
  const location = useLocation();

  useEffect(() => {
    // Initialize Netlify Identity when the component mounts
    netlifyIdentity.init();

    // Set up event listeners for Netlify Identity
    netlifyIdentity.on('init', (currentUser) => {
      setUser(currentUser);
    });
    netlifyIdentity.on('login', (currentUser) => {
      setUser(currentUser);
      // Optionally redirect after login, e.g., to the previous page
      // if the login was triggered by attempting to access a restricted page
      if (location.pathname === '/login') { // Only redirect if on our custom login page
        window.location.href = '/'; // Redirect to homepage or previous path
      }
    });
    netlifyIdentity.on('logout', () => setUser(null));
    netlifyIdentity.on('error', err => console.error('Netlify Identity Error:', err));

    return () => {
      netlifyIdentity.off('init');
      netlifyIdentity.off('login');
      netlifyIdentity.off('logout');
      netlifyIdentity.off('error');
    };
  }, [location.pathname]);

  const handleLogin = () => {
    netlifyIdentity.open();
  };

  const handleLogout = () => {
    netlifyIdentity.logout();
  };

  return (
    <>
      <OriginalNavbarContent {...props} />
      <div className={styles.authWidget}>
        {user ? (
          <>
            <span className={styles.welcomeMessage}>Welcome, {user.user_metadata.full_name || user.email}!</span>
            <button className="button button--info" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <button className="button button--primary" onClick={handleLogin}>
            Login
          </button>
        )}
      </div>
    </>
  );
}
