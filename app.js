const products = window.ANUMARA_PRODUCTS || [];
const state = { category: "all", query: "", visible: 24, modalProduct: null, imageIndex: 0 };

const elements = {
  header: document.querySelector(".site-header"),
  menu: document.querySelector(".menu-toggle"),
  nav: document.querySelector(".main-nav"),
  grid: document.querySelector("#product-grid"),
  count: document.querySelector("#result-count"),
  search: document.querySelector("#search-input"),
  empty: document.querySelector("#empty-state"),
  loadMore: document.querySelector("#load-more"),
  modal: document.querySelector("#product-modal"),
  modalImage: document.querySelector("#modal-image"),
  modalTitle: document.querySelector("#modal-title"),
  modalCategory: document.querySelector("#modal-category"),
  modalMaterials: document.querySelector("#modal-materials"),
  modalThumbs: document.querySelector("#modal-thumbnails"),
  modalWhatsapp: document.querySelector("#modal-whatsapp"),
};

const normalize = value => value
  .normalize("NFD")
  .replace(/[\u0300-\u036f]/g, "")
  .toLowerCase()
  .trim();

function filteredProducts() {
  const query = normalize(state.query);
  return products.filter(product => {
    const matchesCategory = state.category === "all" || product.category === state.category;
    const matchesQuery = !query || normalize(product.search).includes(query);
    return matchesCategory && matchesQuery;
  });
}

function productCard(product, index) {
  const materials = product.materials.length
    ? product.materials.join(" · ")
    : "Pieza artesanal Anumara";
  const badge = product.images.length > 1
    ? `<span class="product-badge">${product.images.length} fotos</span>`
    : "";
  return `
    <article class="product-card" style="animation-delay:${Math.min(index * 35, 350)}ms">
      <button class="product-image-wrap" type="button" data-product="${product.id}" aria-label="Ver ${product.title}">
        ${badge}
        <img src="${product.images[0]}" alt="${product.title}" loading="lazy" width="600" height="800">
      </button>
      <div class="product-info">
        <p class="product-category">${product.categoryLabel}</p>
        <h3 class="product-title">${product.title}</h3>
        <p class="product-materials" title="${materials}">${materials}</p>
      </div>
    </article>`;
}

function render() {
  const matches = filteredProducts();
  const visible = matches.slice(0, state.visible);
  elements.grid.innerHTML = visible.map(productCard).join("");
  elements.count.textContent = matches.length;
  elements.empty.hidden = matches.length > 0;
  elements.loadMore.hidden = state.visible >= matches.length;
}

function setCategory(category, scroll = false) {
  state.category = category;
  state.visible = 24;
  document.querySelectorAll("[data-category]").forEach(button => {
    button.classList.toggle("active", button.dataset.category === category);
  });
  render();
  if (scroll) {
    document.querySelector("#coleccion").scrollIntoView({ behavior: "smooth" });
  }
}

function showModal(product) {
  state.modalProduct = product;
  state.imageIndex = 0;
  elements.modalTitle.textContent = product.title;
  elements.modalCategory.textContent = product.categoryLabel;
  elements.modalMaterials.innerHTML = product.materials.length
    ? product.materials.map(material => `<span>${material}</span>`).join("")
    : "<span>Pieza artesanal Anumara</span>";
  elements.modalWhatsapp.href = product.whatsapp;
  elements.modalThumbs.innerHTML = product.images.map((image, index) => `
    <button type="button" data-image-index="${index}" aria-label="Ver foto ${index + 1}" class="${index === 0 ? "active" : ""}">
      <img src="${image}" alt="" loading="lazy">
    </button>`).join("");
  elements.modal.querySelectorAll(".gallery-nav").forEach(button => {
    button.hidden = product.images.length < 2;
  });
  updateModalImage();
  elements.modal.showModal();
  document.body.classList.add("modal-open");
}

function updateModalImage() {
  const product = state.modalProduct;
  if (!product) return;
  elements.modalImage.src = product.images[state.imageIndex];
  elements.modalImage.alt = `${product.title}, foto ${state.imageIndex + 1} de ${product.images.length}`;
  elements.modalThumbs.querySelectorAll("button").forEach((button, index) => {
    button.classList.toggle("active", index === state.imageIndex);
  });
}

function changeModalImage(direction) {
  const length = state.modalProduct.images.length;
  state.imageIndex = (state.imageIndex + direction + length) % length;
  updateModalImage();
}

document.querySelectorAll("[data-category]").forEach(button => {
  button.addEventListener("click", () => setCategory(button.dataset.category));
});

document.querySelectorAll("[data-jump-category]").forEach(button => {
  button.addEventListener("click", () => setCategory(button.dataset.jumpCategory, true));
});

elements.search.addEventListener("input", event => {
  state.query = event.target.value;
  state.visible = 24;
  render();
});

elements.loadMore.addEventListener("click", () => {
  state.visible += 24;
  render();
});

document.querySelector("#clear-search").addEventListener("click", () => {
  state.query = "";
  elements.search.value = "";
  setCategory("all");
});

elements.grid.addEventListener("click", event => {
  const trigger = event.target.closest("[data-product]");
  if (!trigger) return;
  const product = products.find(item => item.id === trigger.dataset.product);
  if (product) showModal(product);
});

elements.modal.querySelector(".modal-close").addEventListener("click", () => elements.modal.close());
elements.modal.querySelector(".prev").addEventListener("click", () => changeModalImage(-1));
elements.modal.querySelector(".next").addEventListener("click", () => changeModalImage(1));
elements.modalThumbs.addEventListener("click", event => {
  const trigger = event.target.closest("[data-image-index]");
  if (!trigger) return;
  state.imageIndex = Number(trigger.dataset.imageIndex);
  updateModalImage();
});
elements.modal.addEventListener("click", event => {
  if (event.target === elements.modal) elements.modal.close();
});
elements.modal.addEventListener("close", () => {
  document.body.classList.remove("modal-open");
  state.modalProduct = null;
});

elements.menu.addEventListener("click", () => {
  const open = elements.menu.classList.toggle("open");
  elements.nav.classList.toggle("open", open);
  elements.menu.setAttribute("aria-expanded", open);
});
elements.nav.addEventListener("click", () => {
  elements.menu.classList.remove("open");
  elements.nav.classList.remove("open");
  elements.menu.setAttribute("aria-expanded", "false");
});

window.addEventListener("scroll", () => elements.header.classList.toggle("scrolled", scrollY > 20), { passive: true });

const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: .12 });
document.querySelectorAll(".reveal").forEach(element => revealObserver.observe(element));

document.querySelector("#year").textContent = new Date().getFullYear();
if (products.length) {
  const featured = products.find(product => product.title.includes("Corazón Radiante")) || products[0];
  const image = featured.images[1] || featured.images[0];
  const hero = document.querySelector("#hero-product");
  hero.src = image;
  hero.alt = featured.title;
}
render();
