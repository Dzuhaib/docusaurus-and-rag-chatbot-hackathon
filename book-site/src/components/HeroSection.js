import React from 'react';
import clsx from 'clsx';
import styles from './HeroSection.module.css';

export default function HeroSection() {
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className="row">
          <div className={clsx('col col--6', styles.heroText)}>
            <h1 className="hero__title">Physical AI & Humanoid Robotics</h1>
            <p className="hero__subtitle">Bridging the gap between the digital brain and the physical body.</p>
            <div className={styles.buttons}>
              <a
                id="hero-button"
                className="button button--secondary button--lg"
                href="/docs/intro">
                Get Started
              </a>
            </div>
          </div>
          <div className={clsx('col col--6', styles.heroImage)}>
            <img src="/img/Robotics_books.png" alt="Robotics Book" className={styles.bookAnimation} />
          </div>
        </div>
      </div>
    </header>
  );
}
