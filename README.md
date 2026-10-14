# Anumara · Joyería con alma

Tienda estática de Anumara preparada para GitHub Pages. Los pedidos se envían por WhatsApp.

## Actualizar el catálogo

1. Agrega o modifica fotografías en las carpetas originales de collares, pulseras o anillos.
2. Ejecuta:

```powershell
py build_store.py
```

El script reconstruye `products.js` y las imágenes optimizadas en `assets/products/`.

## Vista local

```powershell
py -m http.server 8000
```

Después abre `http://localhost:8000`.
