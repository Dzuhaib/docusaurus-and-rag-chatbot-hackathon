import React, { useEffect, useState } from 'react';
import netlifyIdentity from 'netlify-identity-widget';
import { Redirect, useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function AuthWrapper({ children, restricted }) {
  const {
    siteConfig: { baseUrl },
  } = useDocusaurusContext();
  const location = useLocation();
  const [user, setUser] = useState(netlifyIdentity.currentUser());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // netlifyIdentity.init() is already called in NavbarContent, but it's safe to call again
    // It will ensure the widget is initialized and user state is updated
    netlifyIdentity.init(); 

    netlifyIdentity.on('init', (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    netlifyIdentity.on('login', (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    netlifyIdentity.on('logout', () => {
      setUser(null);
      setLoading(false);
    });

    // Handle initial state if user is already logged in before init event fires
    if (netlifyIdentity.currentUser()) {
      setUser(netlifyIdentity.currentUser());
      setLoading(false);
    } else {
      // If no user and not restricted, still set loading to false
      if (!restricted) {
        setLoading(false);
      }
    }


    return () => {
      netlifyIdentity.off('init');
      netlifyIdentity.off('login');
      netlifyIdentity.off('logout');
    };
  }, []);

  if (!restricted) {
    return <>{children}</>;
  }

  // If content is restricted
  if (loading) {
    return <div>Loading authentication status...</div>; // Or a spinner
  }

  if (!user) {
    // User is not authenticated, redirect to login or show message
    // Use the /login page if defined, otherwise just display a message
    const loginPath = `${baseUrl.endsWith('/') ? baseUrl : baseUrl + '/'}login`;
    
    // Avoid infinite redirects if already on the login page or a page meant to handle login
    if (location.pathname === loginPath) {
      return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <h1>Access Denied</h1>
          <p>You need to be logged in to view this content.</p>
          <button className="button button--primary" onClick={() => netlifyIdentity.open()}>
            Login
          </button>
        </div>
      );
    }
    
    // Redirect to a custom login page
    return <Redirect to={loginPath} />;
  }

  // User is authenticated and content is restricted
  return <>{children}</>;
}
