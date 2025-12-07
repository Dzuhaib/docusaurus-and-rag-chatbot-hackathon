import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Contextual Answers (RAG)',
    Svg: () => (
      <svg className={styles.featureIcon} xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20v2.5a2.5 2.5 0 0 1-2.5 2.5H6.5A2.5 2.5 0 0 1 4 19.5z"></path>
        <path d="M14.5 7.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"></path>
        <path d="M5 12.5V17h14V5H6.5a2.5 2.5 0 0 0-2.5 2.5z"></path>
      </svg>
    ),
    description: (
      <>
        Answers questions about the book using Retrieval Augmented Generation (RAG).
        Highlight text to ask specific questions about it.
      </>
    ),
  },
  {
    title: 'Source Citations',
    Svg: () => (
      <svg className={styles.featureIcon} xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07L9.5 5.5"></path>
        <path d="M11 11.5L12 10.5"></path>
        <path d="M13 10.5L14 9.5"></path>
        <path d="M16 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8l-5-5z"></path>
        <path d="M17 21v-3"></path>
        <path d="M17 18h3"></path>
      </svg>
    ),
    description: (
      <>
        Provides links to the exact sections of the book where the information was retrieved from,
        allowing you to verify and explore further.
      </>
    ),
  },
  {
    title: 'Conversation History',
    Svg: () => (
      <svg className={styles.featureIcon} xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        <path d="M10 8h.01"></path>
        <path d="M14 8h.01"></path>
      </svg>
    ),
    description: (
      <>
        Remembers previous turns in your conversation, enabling natural follow-up questions
        and a more coherent chat experience.
      </>
    ),
  },
  {
    title: 'Streaming Responses',
    Svg: () => (
      <svg className={styles.featureIcon} xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="21 8 21 16 3 16 3 8"></polyline>
        <line x1="10" y1="11" x2="10" y2="11"></line>
        <line x1="14" y1="11" x2="14" y2="11"></line>
      </svg>
    ),
    description: (
      <>
        Answers are streamed in real-time, displaying text as it's generated, providing a
        faster and more interactive user experience.
      </>
    ),
  },
  {
    title: 'User Feedback',
    Svg: () => (
      <svg className={styles.featureIcon} xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07L9.5 5.5"></path>
        <path d="M11 11.5L12 10.5"></path>
        <path d="M13 10.5L14 9.5"></path>
        <path d="M16 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8l-5-5z"></path>
        <path d="M17 21v-3"></path>
        <path d="M17 18h3"></path>
      </svg>
    ),
    description: (
      <>
        Rate answers with a simple thumbs up/down, helping to improve the chatbot's
        performance over time.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
