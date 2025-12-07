import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import netlifyIdentity from 'netlify-identity-widget';

export default function LoginPage() {
  useEffect(() => {
    netlifyIdentity.init();
    netlifyIdentity.open(); // Automatically open the login modal

    return () => {
      netlifyIdentity.off('init');
    };
  }, []);

  return (
    <Layout
      title="Login"
      description="Login to access restricted content">
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3 text--center">
            <h1>Login to Access Restricted Content</h1>
            <p>Please use the Netlify Identity widget to log in.</p>
            <p>
              If the login modal does not appear automatically, please click{' '}
              <button className="button button--primary" onClick={() => netlifyIdentity.open()}>
                here
              </button>
              .
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}
