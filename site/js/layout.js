document.addEventListener('DOMContentLoaded', function () {
  const mainContent = document.querySelector('main.page-content');
  if (!mainContent) return;

  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  const body = document.body;
  const pageKey = currentPath === '/' ? 'home' : currentPath.replace(/^\//, '').replace('.html', '').replace(/[^a-z0-9-]/gi, '-');
  body.classList.add('page-' + pageKey);

  const navItems = [
    { href: '/publications.html', label: 'Publications' },
    { href: '/projects.html', label: 'Projects' },
    { href: '/experiences.html', label: 'Experiences' },
    { href: '/cv.html', label: 'CV' },
    { href: '/accomplishments.html', label: 'Accomplishments' },
    { href: '/bucket-list.html', label: 'Bucket List' },
    { href: '/photography.html', label: 'Photography' }
  ];

  const topbar = document.createElement('div');
  topbar.className = 'topbar';

  const topbarInner = document.createElement('div');
  topbarInner.className = 'inner';

  const brand = document.createElement('a');
  brand.className = 'brand';
  brand.href = '/';
  brand.textContent = "Aiyub's Home page";

  const nav = document.createElement('nav');
  nav.id = 'navlinks';
  nav.className = 'navlinks';

  navItems.forEach(function (item) {
    const link = document.createElement('a');
    link.href = item.href;
    link.textContent = item.label;
    if (currentPath === item.href) {
      link.classList.add('active');
    }
    nav.appendChild(link);
  });

  topbarInner.appendChild(brand);
  topbarInner.appendChild(nav);
  topbar.appendChild(topbarInner);

  const siteContainer = document.createElement('div');
  siteContainer.className = 'site-container';

  const mainLayout = document.createElement('div');
  mainLayout.className = 'main-layout';

  const sidebar = document.createElement('aside');
  sidebar.className = 'profile-sidebar';
  sidebar.innerHTML = `
    <div class="photo-wrap"><img class="profile-photo" src="/images/aiyub.jpeg" alt="Aiyub Ali"></div>
    <div class="name">Md Aiyub Ali</div>
    <div class="pronouns">He/Him</div>
    <ul class="meta">
      <li><i class="fa fa-map-marker-alt"></i> Dhaka, Bangladesh</li>
      <li><i class="fa fa-university"></i> University of Queensland</li>
      <li><i class="fa fa-envelope"></i> <a href="mailto:aiyubali15-13456@diu.edu.bd">Email</a></li>
      <li><i class="fa fa-graduation-cap"></i> <a href="https://scholar.google.com/citations?user=7TGnxUMAAAAJ" target="_blank" rel="noopener">Google Scholar</a></li>
      <li><i class="fa-brands fa-github"></i> <a href="https://github.com/mdaiyub" target="_blank" rel="noopener">Github</a></li>
      <li><i class="fa-brands fa-linkedin"></i> <a href="https://www.linkedin.com/in/md-aiyub-ali-b60173196/" target="_blank" rel="noopener">LinkedIn</a></li>
    </ul>
  `;

  const footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.innerHTML = `
    <div class="footer-container">
      <p class="footer-sitemap">Sitemap</p>
      <p class="footer-follow">
        <strong>FOLLOW:</strong>
        <i class="fa-brands fa-github"></i>
        <a href="https://github.com/mdaiyub" target="_blank">GitHub</a>
      </p>
      <p class="footer-copy">
        © 2026 Aiyub Ali. Powered by Jekyll & AcademicPages, a fork of Minimal Mistakes.
      </p>
    </div>
  `;

  body.insertBefore(topbar, mainContent);
  body.insertBefore(siteContainer, mainContent);

  mainLayout.appendChild(sidebar);
  mainLayout.appendChild(mainContent);
  siteContainer.appendChild(mainLayout);

  body.appendChild(footer);
});