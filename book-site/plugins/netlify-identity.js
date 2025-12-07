// book-site/plugins/netlify-identity.js
module.exports = function (context, options) {
  return {
    name: 'netlify-identity-plugin',
    injectHtmlTags() {
      return {
        headTags: [
          {
            tagName: 'script',
            attributes: {
              src: 'https://identity.netlify.com/v1/netlify-identity-widget.js',
            },
          },
        ],
        postBodyTags: [
          {
            tagName: 'script',
            innerHTML: `
              if (window.netlifyIdentity) {
                window.netlifyIdentity.on("init", user => {
                  if (!user) {
                    window.netlifyIdentity.on("login", () => {
                      document.location.href = "/admin/";
                    });
                  }
                });
              }
            `,
          },
        ],
      };
    },
  };
};
