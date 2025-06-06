document.addEventListener('DOMContentLoaded', function () {
  (function() {
    "use strict";

    function toggleScrolled() {
      const selectBody = document.querySelector('body');
      const selectHeader = document.querySelector('#header');
      if (!selectBody || !selectHeader) return;
      if (!selectHeader.classList.contains('scroll-up-sticky') &&
          !selectHeader.classList.contains('sticky-top') &&
          !selectHeader.classList.contains('fixed-top')) return;
      window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
    }

    document.addEventListener('scroll', toggleScrolled);
    window.addEventListener('load', toggleScrolled);

    const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

    function mobileNavToogle() {
      const body = document.querySelector('body');
      if (!body) return;
      body.classList.toggle('mobile-nav-active');
      if (mobileNavToggleBtn) {
        mobileNavToggleBtn.classList.toggle('bi-list');
        mobileNavToggleBtn.classList.toggle('bi-x');
      }
    }

    if (mobileNavToggleBtn) {
      mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
    }

    const navMenuLinks = document.querySelectorAll('#navmenu a');
    if (navMenuLinks.length > 0) {
      navMenuLinks.forEach(navmenu => {
        navmenu.addEventListener('click', () => {
          if (document.querySelector('.mobile-nav-active')) {
            mobileNavToogle();
          }
        });
      });
    }

    const toggleDropdowns = document.querySelectorAll('.navmenu .toggle-dropdown');
    if (toggleDropdowns.length > 0) {
      toggleDropdowns.forEach(navmenu => {
        navmenu.addEventListener('click', function(e) {
          e.preventDefault();
          if (!this.parentNode || !this.parentNode.nextElementSibling) return;
          this.parentNode.classList.toggle('active');
          this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
          e.stopImmediatePropagation();
        });
      });
    }

    let scrollTop = document.querySelector('.scroll-top');

    function toggleScrollTop() {
      if (!scrollTop) return;
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }

    if (scrollTop) {
      scrollTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }

    window.addEventListener('load', toggleScrollTop);
    document.addEventListener('scroll', toggleScrollTop);

    function aosInit() {
      if (typeof AOS !== 'undefined') {
        AOS.init({
          duration: 600,
          easing: 'ease-in-out',
          once: true,
          mirror: false
        });
      }
    }

    window.addEventListener('load', aosInit);

    if (typeof GLightbox !== 'undefined') {
      GLightbox({ selector: '.glightbox' });
    }

    function initSwiper() {
      const swiperElements = document.querySelectorAll(".init-swiper");
      if (swiperElements.length > 0) {
        swiperElements.forEach(function(swiperElement) {
          const configElement = swiperElement.querySelector(".swiper-config");
          if (!configElement) return;
          let config = JSON.parse(configElement.innerHTML.trim());
          if (swiperElement.classList.contains("swiper-tab")) {
            if (typeof initSwiperWithCustomPagination !== 'undefined') {
              initSwiperWithCustomPagination(swiperElement, config);
            }
          } else if (typeof Swiper !== 'undefined') {
            new Swiper(swiperElement, config);
          }
        });
      }
    }

    window.addEventListener("load", initSwiper);

    if (typeof PureCounter !== 'undefined') {
      new PureCounter();
    }

    const faqItems = document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle');
    if (faqItems.length > 0) {
      faqItems.forEach((faqItem) => {
        faqItem.addEventListener('click', () => {
          if (faqItem.parentNode) {
            faqItem.parentNode.classList.toggle('faq-active');
          }
        });
      });
    }

    window.addEventListener('load', function(e) {
      if (window.location.hash) {
        const section = document.querySelector(window.location.hash);
        if (section) {
          setTimeout(() => {
            let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
            window.scrollTo({
              top: section.offsetTop - parseInt(scrollMarginTop),
              behavior: 'smooth'
            });
          }, 100);
        }
      }
    });

    let navmenulinks = document.querySelectorAll('.navmenu a');

    function navmenuScrollspy() {
      if (navmenulinks.length === 0) return;
      navmenulinks.forEach(navmenulink => {
        if (!navmenulink.hash) return;
        let section = document.querySelector(navmenulink.hash);
        if (!section) return;
        let position = window.scrollY + 200;
        if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
          document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
          navmenulink.classList.add('active');
        } else {
          navmenulink.classList.remove('active');
        }
      });
    }

    window.addEventListener('load', navmenuScrollspy);
    document.addEventListener('scroll', navmenuScrollspy);

  })();
});