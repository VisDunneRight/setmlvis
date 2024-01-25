export default {
  title: "SetMLVis",
  description: "Documentation for an interactive object detection model comparison tool: SetMLVis",
  lang: 'en-US',
  cleanUrls: true,
  // If this is disabled, when building it it will give deadlink errors if your markdown has the wrong links
  ignoreDeadLinks: true,
  
  themeConfig: {
    base: '/setmlvis/',
    logo: "/logo-translucent.svg",
    siteTitle: "SetMLVis",
    search: {
      provider: "local",
    },
    // Navbar Link
    nav: [
      { text: "About", link: "/about" },
      { text: "Contact", link: "/contact" },
      { text: "Guide", link: "/guide/" },
      
    ],
    // Social Icons
    socialLinks: [
      { icon: "github", link: "https://github.com/VisDunneRight/setmlvis" },
      
    ],
    // Sidebar
   sidebar: {
    
    "/guide/": [
      {
        text: 'Introduction',
        collapsed: false,
        items: [
          { text: 'What is SetMLVis', link: '/guide/' },
          { text: 'Getting Started', link: '/guide/getting_started.md' },
        ]
      },
      {
        text: 'Using SetMLVis',
        collapsed: false,
        items: [
          { text: 'Object Detection Datasets',
            collapsed: false,
            items: [
            { text: 'Data Input', link: '/guide/first_steps.md' },
            { text: 'CreateSetJson', link: '/guide/using_selections.md' },
            ]
          },
          { text: 'User Interface',
            collapsed: false,
            items: [
            { text: 'Overview', link: '/guide/prefabs/planetext.md' },
            { text: 'Set Visualization', link: '/guide/prefabs/axes.md' },
            { text: 'Thumbnail View', link: '/guide/prefabs/chromatic.md'},
            { text: 'Detail View View', link: '/guide/prefabs/chromatic.md'}
            ]
          },
          {
            text: 'Miscellaneous',link: '/guide/prefabs/planetext.md' },

          
  
         
        ]
      },
      // {
      //   text: 'Prefabs',
      //   collapsed: true,
      //   items: [
      //     { text: 'WIP', link: '' }
      //   ]
      // },
      // {
      //   text: 'Interactions',
      //   collapsed: true,
      //   items: [
      //     { text: 'WIP', link: '' }
      //   ]
      // },
      

    ],
    
  },
   
    // you can disable the previous and next page here
    docFooter: {
      prev: false,
      next: true,
    },
    editLink: {
      pattern: 'https://github.com/Evavic44/adocs/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },
    footer: {
      message: "Released under the MIT License.",
      copyright: "Copyright © 2024-present Adocs",
    },
    markdown: {
      theme: "material-palenight",
      lineNumbers: true,
    },
    // Mobile Config only
    returnToTopLabel: 'Go to Top',
    sidebarMenuLabel: 'Menu',
  },
};
