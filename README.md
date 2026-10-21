# Anumara · Joyería con alma

Tienda estática de Anumara preparada para GitHub Pages. Los pedidos se envían por WhatsApp.

## Pagos con Mercado Pago y transferencia bancaria (México)

La ficha de cada pieza y la sección de contacto permiten abrir el enlace general
**https://link.mercadopago.com.mx/anumara** en otra pestaña.
Mercado Pago captura los datos de la tarjeta; esta web no los recibe ni necesita
Access Tokens. No es un carrito ni una integración de Checkout Pro.

También se aceptan transferencias bancarias a la **CLABE 072540012957205984**.
La CLABE se muestra en contacto y en la ficha de cada producto. Su formato y
dígito verificador son válidos; esto no acredita la titularidad ni el estado
de la cuenta. El cliente envía el comprobante al WhatsApp **(+52) 777 189 90 45**.

### Flujo de compra

1. El cliente confirma por WhatsApp el precio de la fotografía y la disponibilidad.
2. Calcula el monto a pagar por Mercado Pago o transferencia bancaria: precio de
   las piezas más el envío que corresponda. **Envío gratis a partir de $3,000.00 MXN
   en joyería** (incluye exactamente $3,000.00); por debajo, agrega **$300 MXN por
   pedido**, no por pieza. El umbral se calcula sin incluir el envío.
   Ejemplos: $1,500 + $300 = $1,800; $2,999.99 + $300 = $3,299.99;
   $3,000 + $0 = $3,000; $3,500 + $0 = $3,500 MXN.
   La tienda no extrae precios de las imágenes ni calcula o transmite el monto.
3. Verifica los datos del destinatario y transfiere a la CLABE indicada, o abre
   Mercado Pago, escribe manualmente el monto y paga con sus medios disponibles.
4. Usa «Enviar comprobante por WhatsApp» en la ficha. El mensaje incluye nombre
   y código de la pieza, pero **no afirma que el pago esté confirmado**.
5. Adjunta manualmente una captura o comprobante en WhatsApp al
   **(+52) 777 189 90 45**, e indica las piezas del pedido y los datos de entrega.
   El botón no adjunta archivos ni envía mensajes automáticamente.
6. Anumara verifica el abono y el monto en su cuenta bancaria o de Mercado Pago,
   según el medio elegido, antes de concretar el envío.

### Operación y entrega

- Confirma que tu cuenta personal esté habilitada para recibir pagos y que los
  datos del vendedor sean los que deben ver tus clientes. Revisa comisiones,
  plazos de disponibilidad y medios de pago en tu cuenta de Mercado Pago.
- El monto es abierto: verifica que el importe recibido cubra las piezas y,
  únicamente si la joyería suma menos de $3,000.00 MXN, los $300 MXN de envío.
- Acuerda por WhatsApp el destinatario, dirección y condiciones de entrega.
- Verifica el pago **en tu cuenta bancaria o de Mercado Pago** antes de enviar; una captura
  de pantalla o un mensaje del comprador no demuestra el pago.
- No hay confirmación automática ni reserva de inventario. Actualiza el catálogo
  al vender una pieza única. El enlace general se comparte entre todas las piezas.
- Si cambias el enlace, la CLABE o el envío, actualiza las dos ubicaciones de `index.html`
  (contacto y ficha de producto) y esta documentación.

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
