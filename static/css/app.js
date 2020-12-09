const navSlide = () => {
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav-links');
  const navLinks = document.querySelectorAll('.nav-links li');

  burger.addEventListener('click', () => {
    //Toggle Nav
    nav.classList.toggle('nav-active');
    //Animate links
    navLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = ''
      } else {
        link.style.animation = `navLinkFade 0.25s ease forwards 0.3s`;
      }
    });
    //Burger animation
    burger.classList.toggle('toggle')
  });
}

navSlide();
