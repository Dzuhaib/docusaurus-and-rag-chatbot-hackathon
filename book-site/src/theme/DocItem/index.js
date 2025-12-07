import React from 'react';
import DocItem from '@theme-original/DocItem';
import AuthWrapper from '@site/src/components/AuthWrapper';

export default function DocItemWrapper(props) {
  const { content } = props;
  const { metadata } = content;
  const isRestricted = metadata.frontMatter.restricted || false;

  return (
    <AuthWrapper restricted={isRestricted}>
      <DocItem {...props} />
    </AuthWrapper>
  );
}
