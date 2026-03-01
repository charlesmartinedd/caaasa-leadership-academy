import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Colors
const NAVY = rgb(0.102, 0.212, 0.365);    // #1a365d
const GOLD = rgb(0.788, 0.635, 0.153);    // #c9a227
const WHITE = rgb(1, 1, 1);
const LIGHT_GRAY = rgb(0.92, 0.92, 0.92);
const DARK_GRAY = rgb(0.25, 0.25, 0.25);
const DOTTED_GRAY = rgb(0.75, 0.75, 0.75);

async function createHandout() {
  const doc = await PDFDocument.create();
  // Landscape letter: 792 x 612
  const page = doc.addPage([792, 612]);
  const { width, height } = page.getSize();

  const fontBold = await doc.embedFont(StandardFonts.HelveticaBold);
  const fontReg = await doc.embedFont(StandardFonts.Helvetica);
  const fontItalic = await doc.embedFont(StandardFonts.HelveticaOblique);

  const margin = 28;

  // === HEADER BAR (Gold) ===
  page.drawRectangle({ x: 0, y: height - 50, width, height: 50, color: GOLD });
  page.drawText('AI CREATOR LAB', {
    x: margin, y: height - 35, size: 18, font: fontBold, color: NAVY
  });
  page.drawText('Creator Blueprint', {
    x: margin + fontBold.widthOfTextAtSize('AI CREATOR LAB  ', 18),
    y: height - 35, size: 18, font: fontReg, color: NAVY
  });
  // Logos placeholder right side
  page.drawText('CAAASA x TRPEC', {
    x: width - margin - fontReg.widthOfTextAtSize('CAAASA x TRPEC', 10),
    y: height - 33, size: 10, font: fontReg, color: NAVY
  });

  // === NAME + QUEST ROW ===
  const nameY = height - 72;
  page.drawText('Name:', { x: margin, y: nameY, size: 11, font: fontBold, color: DARK_GRAY });
  page.drawLine({ start: { x: margin + 40, y: nameY - 2 }, end: { x: 240, y: nameY - 2 },
    thickness: 0.5, color: DARK_GRAY });

  page.drawText('Quest:', { x: 260, y: nameY, size: 11, font: fontBold, color: DARK_GRAY });
  // Checkboxes
  const quests = ['Sound', 'Meme', 'Video'];
  let qx = 305;
  for (const q of quests) {
    page.drawRectangle({ x: qx, y: nameY - 2, width: 11, height: 11,
      borderColor: DARK_GRAY, borderWidth: 1, color: WHITE });
    page.drawText(q, { x: qx + 14, y: nameY, size: 10, font: fontReg, color: DARK_GRAY });
    qx += 14 + fontReg.widthOfTextAtSize(q, 10) + 14;
  }

  // === MAIN CONTENT AREA ===
  const contentTop = nameY - 20;
  const contentBottom = 50;
  const contentHeight = contentTop - contentBottom;
  const midX = width / 2 + 10;

  // Divider lines
  page.drawLine({ start: { x: midX - 10, y: contentTop }, end: { x: midX - 10, y: contentBottom },
    thickness: 0.5, color: LIGHT_GRAY });
  page.drawLine({ start: { x: margin, y: contentTop - contentHeight / 2 },
    end: { x: midX - 20, y: contentTop - contentHeight / 2 },
    thickness: 0.5, color: LIGHT_GRAY });
  page.drawLine({ start: { x: midX, y: contentTop - contentHeight * 0.65 },
    end: { x: width - margin, y: contentTop - contentHeight * 0.65 },
    thickness: 0.5, color: LIGHT_GRAY });

  // --- SECTION 1: VIBE CHECK (top-left) ---
  const s1y = contentTop - 4;
  page.drawRectangle({ x: margin - 2, y: s1y - 12, width: 90, height: 14, color: GOLD });
  page.drawText('1. VIBE CHECK', { x: margin, y: s1y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('Who is this for?', { x: margin, y: s1y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  page.drawLine({ start: { x: margin, y: s1y - 44 }, end: { x: midX - 24, y: s1y - 44 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });
  page.drawLine({ start: { x: margin, y: s1y - 60 }, end: { x: midX - 24, y: s1y - 60 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });

  page.drawText('What do they care about?', { x: margin, y: s1y - 78, size: 10, font: fontReg, color: DARK_GRAY });
  page.drawLine({ start: { x: margin, y: s1y - 92 }, end: { x: midX - 24, y: s1y - 92 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });
  page.drawLine({ start: { x: margin, y: s1y - 108 }, end: { x: midX - 24, y: s1y - 108 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });

  // --- SECTION 2: THE PROBLEM (bottom-left) ---
  const s2y = contentTop - contentHeight / 2 - 4;
  page.drawRectangle({ x: margin - 2, y: s2y - 12, width: 95, height: 14, color: GOLD });
  page.drawText('2. THE PROBLEM', { x: margin, y: s2y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('What message/feeling?', { x: margin, y: s2y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  page.drawLine({ start: { x: margin, y: s2y - 44 }, end: { x: midX - 24, y: s2y - 44 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });
  page.drawLine({ start: { x: margin, y: s2y - 60 }, end: { x: midX - 24, y: s2y - 60 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });
  page.drawLine({ start: { x: margin, y: s2y - 76 }, end: { x: midX - 24, y: s2y - 76 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });

  // --- SECTION 3: BRAINSTORM (top-right, large sketch area) ---
  const s3y = contentTop - 4;
  const s3x = midX;
  page.drawRectangle({ x: s3x - 2, y: s3y - 12, width: 95, height: 14, color: GOLD });
  page.drawText('3. BRAINSTORM', { x: s3x, y: s3y - 10, size: 10, font: fontBold, color: NAVY });

  // Dotted grid sketch box
  const sketchX = s3x;
  const sketchY = contentTop - contentHeight * 0.65 + 6;
  const sketchW = width - margin - s3x;
  const sketchH = s3y - 20 - sketchY;
  page.drawRectangle({ x: sketchX, y: sketchY, width: sketchW, height: sketchH,
    borderColor: DOTTED_GRAY, borderWidth: 1, color: WHITE });

  // Draw dotted grid inside
  const gridSpacing = 18;
  for (let gy = sketchY + gridSpacing; gy < sketchY + sketchH - 4; gy += gridSpacing) {
    page.drawLine({ start: { x: sketchX + 4, y: gy }, end: { x: sketchX + sketchW - 4, y: gy },
      thickness: 0.3, color: DOTTED_GRAY, dashArray: [1, 4] });
  }
  for (let gx = sketchX + gridSpacing; gx < sketchX + sketchW - 4; gx += gridSpacing) {
    page.drawLine({ start: { x: gx, y: sketchY + 4 }, end: { x: gx, y: sketchY + sketchH - 4 },
      thickness: 0.3, color: DOTTED_GRAY, dashArray: [1, 4] });
  }

  // Label inside sketch
  const labelText = 'Sketch, storyboard, or doodle your idea here';
  const labelW = fontItalic.widthOfTextAtSize(labelText, 9);
  page.drawText(labelText, {
    x: sketchX + (sketchW - labelW) / 2, y: sketchY + 6,
    size: 9, font: fontItalic, color: DOTTED_GRAY
  });

  // --- SECTION 4: BUILD IT (bottom-left under section 2 line, actually bottom-right-left) ---
  const s4y = contentTop - contentHeight * 0.65 - 4;
  page.drawRectangle({ x: s3x - 2, y: s4y - 12, width: 72, height: 14, color: GOLD });
  page.drawText('4. BUILD IT', { x: s3x, y: s4y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('Tool:', { x: s3x, y: s4y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  page.drawLine({ start: { x: s3x + 30, y: s4y - 32 }, end: { x: s3x + 160, y: s4y - 32 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });

  page.drawText('My prompt:', { x: s3x, y: s4y - 48, size: 10, font: fontReg, color: DARK_GRAY });
  page.drawLine({ start: { x: s3x, y: s4y - 62 }, end: { x: s3x + 160, y: s4y - 62 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });
  page.drawLine({ start: { x: s3x, y: s4y - 78 }, end: { x: s3x + 160, y: s4y - 78 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });

  // --- SECTION 5: DROP IT (bottom-right) ---
  const s5x = s3x + 180;
  page.drawRectangle({ x: s5x - 2, y: s4y - 12, width: 68, height: 14, color: GOLD });
  page.drawText('5. DROP IT', { x: s5x, y: s4y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('Feedback I got:', { x: s5x, y: s4y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  page.drawLine({ start: { x: s5x, y: s4y - 44 }, end: { x: width - margin, y: s4y - 44 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });

  page.drawText('One thing I\'d change:', { x: s5x, y: s4y - 60, size: 10, font: fontReg, color: DARK_GRAY });
  page.drawLine({ start: { x: s5x, y: s4y - 74 }, end: { x: width - margin, y: s4y - 74 },
    thickness: 0.5, color: DOTTED_GRAY, dashArray: [2, 2] });

  // === FOOTER BAR (Navy) ===
  page.drawRectangle({ x: 0, y: 0, width, height: 36, color: NAVY });
  const footerText = '"Design with purpose. Create with AI."';
  const ftw = fontItalic.widthOfTextAtSize(footerText, 11);
  page.drawText(footerText, {
    x: (width - ftw) / 2, y: 13, size: 11, font: fontItalic, color: GOLD
  });

  // Save
  const pdfBytes = await doc.save();
  const outPath = path.join(__dirname, 'Creator-Blueprint-Handout.pdf');
  fs.writeFileSync(outPath, pdfBytes);
  console.log('Print handout saved to', outPath);
}

createHandout().catch(err => { console.error(err); process.exit(1); });
