import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link'; // Import Link
import HeroSection from '@site/src/components/HeroSection';
import HomepageFeatures from '@site/src/components/HomepageFeatures'; // Import HomepageFeatures
import clsx from 'clsx'; // Import clsx

function ChaptersSection() {
  const chapters = [
    {
      title: 'The Robotic Nervous System: Foundations of Robot Control',
      link: '/docs/category/the-robotic-nervous-system-foundations-of-robot-control',
    },
    {
      title: 'The Digital Twin: Simulating Robots and Environments',
      link: '/docs/category/the-digital-twin-simulating-robots-and-environments',
    },
    {
      title: 'The Embodied Brain: Perception, Navigation, and Language',
      link: '/docs/category/the-embodied-brain-perception-navigation-and-language',
    },
  ];

  return (
    <section className={clsx('padding-vert--xl', 'chapter-section')}> {/* Add class for styling */}
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2 className={clsx('text--center', 'margin-bottom--xl')}>Book Chapters</h2> {/* Use classes for styling */}
            <div className="row">
              {chapters.map((chapter, idx) => (
                <div key={idx} className="col col--4 margin-bottom--lg">
                  <div className={clsx('card', 'chapterCard')}> {/* Apply chapterCard class */}
                    <div className="card__header">
                      <h3>{chapter.title}</h3>
                    </div>
                    <div className="card__body">
                      <p>Explore this chapter.</p>
                    </div>
                    <div className="card__footer">
                      <Link
                        className="button button--primary button--block"
                        to={chapter.link}>
                        Read Chapter
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <Layout
      title="Home"
      description="A book about Physical AI & Humanoid Robotics">
      <HeroSection />
      <main>
        <ChaptersSection />
        <HomepageFeatures /> {/* Render HomepageFeatures here */}
      </main>
    </Layout>
  );
}
