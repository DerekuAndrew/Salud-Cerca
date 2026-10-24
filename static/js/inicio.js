const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navegacion');

if (menuButton && navigation) {
  menuButton.addEventListener('click', () => {
    const isOpen = navigation.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });

  navigation.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navigation.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
    });
  });
}

const searchInput = document.querySelector('#buscador-especialidades');
const specialtyCards = [...document.querySelectorAll('.specialty-card')];
const emptyMessage = document.querySelector('#sin-resultados');

if (searchInput && specialtyCards.length && emptyMessage) {
  searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim().toLocaleLowerCase('es-MX');
    let visibleCount = 0;

    specialtyCards.forEach((card) => {
      const content = `${card.dataset.search} ${card.textContent}`.toLocaleLowerCase('es-MX');
      const matches = content.includes(query);
      card.hidden = !matches;
      if (matches) visibleCount += 1;
    });

    emptyMessage.hidden = visibleCount > 0;
  });
}
