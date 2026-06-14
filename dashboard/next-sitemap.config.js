/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: 'https://lumina-overmind.com',
  generateRobotsTxt: true,
  outDir: 'out',
  transform: async (config, path) => {
    // Custom transformation if needed
    return {
      loc: path,
      lastmod: new Date().toISOString(),
      changefreq: 'daily',
      priority: 0.7,
    }
  },
  additionalPaths: async (config) => {
    const paths = [
      {
        loc: '/dashboard',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 1.0,
      },
      {
        loc: '/leads',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 0.9,
      },
      {
        loc: '/projects',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 0.9,
      },
      {
        loc: '/inbox',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 0.8,
      },
      {
        loc: '/growth',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 0.8,
      },
      {
        loc: '/geo-intel',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 0.8,
      },
      {
        loc: '/jarvis',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 0.7,
      },
      {
        loc: '/workflows',
        lastmod: new Date().toISOString(),
        changefreq: 'daily',
        priority: 0.7,
      },
    ]
    return paths
  },
}
