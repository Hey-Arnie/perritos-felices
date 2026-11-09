/**
 * PERRITOS FELICES — MOTOR DE CÁPSULAS INTERACTIVAS & SHAREABLE CARDS
 * Cumplimiento estricto Zero-Trust: Cero innerHTML, 100% APIs seguras del DOM
 * Generación nativa en Canvas 2D (4:5 retina) para descarga y compartir
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    initShareableCards();
    initVisualComparators();
  });

  /**
   * Inicializa la generación y compartición de tarjetas TL;DR
   */
  function initShareableCards() {
    const shareCards = document.querySelectorAll('[data-section="tldr-share-card"]');
    if (!shareCards.length) return;

    shareCards.forEach((section) => {
      const container = section.querySelector('.share-card-container');
      const btnDownload = section.querySelector('.btn-download-card');
      const btnShare = section.querySelector('.btn-share-native');

      if (!container) return;

      // Generar imagen en canvas
      async function generateCardImage() {
        const width = 1080;
        const height = 1350;
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        if (!ctx) return null;

        // Extraer datos del DOM con textContent seguro
        const titleEl = container.querySelector('.share-card-title');
        const pillEl = container.querySelector('.share-card-pill');
        const bullets = container.querySelectorAll('.share-card-bullet');
        const brandName = 'Perritos Felices';
        const slogan = 'Ladridos que inspiran • www.perritosfelices.com';

        const titleText = titleEl ? titleEl.textContent.trim() : 'Cápsula Informativa';
        const pillText = pillEl ? pillEl.textContent.trim() : 'TL;DR 30s';

        // 1. Fondo Crema Editorial
        ctx.fillStyle = '#FDFBF7';
        ctx.fillRect(0, 0, width, height);

        // 2. Borde exterior Neobrutalista
        ctx.lineWidth = 14;
        ctx.strokeStyle = '#10152B';
        ctx.strokeRect(40, 40, width - 80, height - 80);

        // 3. Cabecera / Marca
        // Círculo dorado del logo
        ctx.beginPath();
        ctx.arc(110, 120, 36, 0, Math.PI * 2);
        ctx.fillStyle = '#FDB54A';
        ctx.fill();
        ctx.lineWidth = 4;
        ctx.strokeStyle = '#10152B';
        ctx.stroke();

        // Nombre de marca
        ctx.fillStyle = '#10152B';
        ctx.font = 'bold 36px "Inter", sans-serif';
        ctx.fillText(brandName, 170, 132);

        // Pastilla TL;DR
        ctx.fillStyle = '#FDB54A';
        ctx.beginPath();
        ctx.roundRect(width - 290, 95, 180, 52, 26);
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = '#10152B';
        ctx.stroke();

        ctx.fillStyle = '#10152B';
        ctx.font = 'bold 22px "Space Mono", monospace';
        ctx.fillText(pillText, width - 265, 130);

        // Línea divisoria punteada
        ctx.setLineDash([12, 10]);
        ctx.strokeStyle = 'rgba(16, 21, 43, 0.25)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(70, 190);
        ctx.lineTo(width - 70, 190);
        ctx.stroke();
        ctx.setLineDash([]);

        // 4. Titular Principal
        ctx.fillStyle = '#10152B';
        ctx.font = 'bold 56px "Fraunces", Georgia, serif';
        wrapText(ctx, titleText, 80, 280, width - 160, 68);

        // 5. Bullets Clínicos / Puntos Clave
        let yPos = 520;
        bullets.forEach((bullet) => {
          const text = bullet.textContent.replace(/^[✔✘ℹ•\s]+/, '').trim();
          
          // Badge circular de viñeta
          ctx.beginPath();
          ctx.arc(110, yPos - 12, 20, 0, Math.PI * 2);
          ctx.fillStyle = '#E8EDFF';
          ctx.fill();
          ctx.lineWidth = 2.5;
          ctx.strokeStyle = '#2C4BCA';
          ctx.stroke();

          // Check mark
          ctx.fillStyle = '#2C4BCA';
          ctx.font = 'bold 24px "Inter", sans-serif';
          ctx.fillText('✔', 101, yPos - 4);

          // Texto del punto clave
          ctx.fillStyle = '#3D4463';
          ctx.font = '500 32px "Inter", sans-serif';
          const linesDrawn = wrapText(ctx, text, 150, yPos, width - 250, 44);
          yPos += (linesDrawn * 44) + 40;
        });

        // 6. Pie de tarjeta
        ctx.setLineDash([12, 10]);
        ctx.strokeStyle = 'rgba(16, 21, 43, 0.25)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(70, height - 150);
        ctx.lineTo(width - 70, height - 150);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = '#575E7E';
        ctx.font = 'bold 24px "Space Mono", monospace';
        ctx.fillText(slogan, 80, height - 90);

        return new Promise((resolve) => {
          canvas.toBlob((blob) => resolve(blob), 'image/png');
        });
      }

      // Manejador: Descarga directa
      if (btnDownload) {
        btnDownload.addEventListener('click', async () => {
          const originalText = btnDownload.textContent;
          btnDownload.textContent = '⏳ Generando...';
          btnDownload.disabled = true;

          try {
            const blob = await generateCardImage();
            if (blob) {
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'perritos_felices_tldr_capsula.png';
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
              URL.revokeObjectURL(url);
            }
          } catch (err) {
            console.error('Error al generar tarjeta:', err);
          } finally {
            btnDownload.textContent = originalText;
            btnDownload.disabled = false;
          }
        });
      }

      // Manejador: Compartir nativo
      if (btnShare) {
        btnShare.addEventListener('click', async () => {
          try {
            const blob = await generateCardImage();
            if (blob && navigator.canShare && navigator.canShare({ files: [new File([blob], 'capsula.png', { type: 'image/png' })] })) {
              const file = new File([blob], 'perritos_felices_capsula.png', { type: 'image/png' });
              await navigator.share({
                title: 'Cápsula Perritos Felices',
                text: 'Mira este resumen clave de bienestar canino.',
                files: [file]
              });
            } else if (navigator.share) {
              await navigator.share({
                title: 'Perritos Felices — Cápsula',
                url: window.location.href
              });
            } else if (btnDownload) {
              btnDownload.click();
            }
          } catch (err) {
            if (err.name !== 'AbortError') {
              console.error('Error al compartir:', err);
            }
          }
        });
      }
    });
  }

  /**
   * Inicializa comparadores visuales y sus filtros
   */
  function initVisualComparators() {
    const comparators = document.querySelectorAll('[data-section="visual-comparator"]');
    if (!comparators.length) return;

    comparators.forEach((comparator) => {
      const filterButtons = comparator.querySelectorAll('.comparator-filter-btn');
      const items = comparator.querySelectorAll('.comparator-item');

      if (!filterButtons.length || !items.length) return;

      filterButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
          const targetFilter = btn.getAttribute('data-filter') || 'all';

          filterButtons.forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');

          items.forEach((item) => {
            if (targetFilter === 'all' || item.classList.contains(`status-${targetFilter}`)) {
              item.style.display = 'flex';
            } else {
              item.style.display = 'none';
            }
          });
        });
      });
    });
  }

  /**
   * Helper seguro para ajustar texto en Canvas multilínea
   */
  function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
    const words = text.split(' ');
    let line = '';
    let lineCount = 0;

    for (let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + ' ';
      const metrics = ctx.measureText(testLine);
      const testWidth = metrics.width;
      if (testWidth > maxWidth && n > 0) {
        ctx.fillText(line.trim(), x, y);
        line = words[n] + ' ';
        y += lineHeight;
        lineCount++;
      } else {
        line = testLine;
      }
    }
    ctx.fillText(line.trim(), x, y);
    lineCount++;
    return lineCount;
  }
})();
