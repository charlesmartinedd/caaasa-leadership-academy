import { PDFDocument, rgb, StandardFonts, PDFTextField, PDFCheckBox } from 'pdf-lib';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const NAVY = rgb(0.102, 0.212, 0.365);
const GOLD = rgb(0.788, 0.635, 0.153);
const WHITE = rgb(1, 1, 1);
const LIGHT_GRAY = rgb(0.92, 0.92, 0.92);
const DARK_GRAY = rgb(0.25, 0.25, 0.25);
const DOTTED_GRAY = rgb(0.75, 0.75, 0.75);
const FIELD_BG = rgb(0.96, 0.96, 0.98);

async function createFillable() {
  const doc = await PDFDocument.create();
  const page = doc.addPage([792, 612]);
  const { width, height } = page.getSize();
  const form = doc.getForm();

  const fontBold = await doc.embedFont(StandardFonts.HelveticaBold);
  const fontReg = await doc.embedFont(StandardFonts.Helvetica);
  const fontItalic = await doc.embedFont(StandardFonts.HelveticaOblique);

  const margin = 28;

  // === HEADER BAR ===
  page.drawRectangle({ x: 0, y: height - 50, width, height: 50, color: GOLD });
  page.drawText('AI CREATOR LAB', { x: margin, y: height - 35, size: 18, font: fontBold, color: NAVY });
  page.drawText('Creator Blueprint', {
    x: margin + fontBold.widthOfTextAtSize('AI CREATOR LAB  ', 18),
    y: height - 35, size: 18, font: fontReg, color: NAVY });
  page.drawText('CAAASA x TRPEC', {
    x: width - margin - fontReg.widthOfTextAtSize('CAAASA x TRPEC', 10),
    y: height - 33, size: 10, font: fontReg, color: NAVY });

  // === NAME + QUEST ROW ===
  const nameY = height - 72;
  page.drawText('Name:', { x: margin, y: nameY, size: 11, font: fontBold, color: DARK_GRAY });

  const nameField = form.createTextField('name');
  nameField.addToPage(page, { x: margin + 42, y: nameY - 5, width: 180, height: 18,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });

  page.drawText('Quest:', { x: 260, y: nameY, size: 11, font: fontBold, color: DARK_GRAY });

  const quests = ['Sound', 'Meme', 'Video'];
  let qx = 305;
  for (const q of quests) {
    const cb = form.createCheckBox(`quest_${q.toLowerCase()}`);
    cb.addToPage(page, { x: qx, y: nameY - 3, width: 12, height: 12,
      borderWidth: 1, borderColor: DARK_GRAY, backgroundColor: WHITE });
    page.drawText(q, { x: qx + 15, y: nameY, size: 10, font: fontReg, color: DARK_GRAY });
    qx += 15 + fontReg.widthOfTextAtSize(q, 10) + 14;
  }

  // === LAYOUT ===
  const contentTop = nameY - 20;
  const contentBottom = 50;
  const contentHeight = contentTop - contentBottom;
  const midX = width / 2 + 10;

  // Dividers
  page.drawLine({ start: { x: midX - 10, y: contentTop }, end: { x: midX - 10, y: contentBottom },
    thickness: 0.5, color: LIGHT_GRAY });
  page.drawLine({ start: { x: margin, y: contentTop - contentHeight / 2 },
    end: { x: midX - 20, y: contentTop - contentHeight / 2 }, thickness: 0.5, color: LIGHT_GRAY });
  page.drawLine({ start: { x: midX, y: contentTop - contentHeight * 0.65 },
    end: { x: width - margin, y: contentTop - contentHeight * 0.65 }, thickness: 0.5, color: LIGHT_GRAY });

  // --- SECTION 1: VIBE CHECK ---
  const s1y = contentTop - 4;
  page.drawRectangle({ x: margin - 2, y: s1y - 12, width: 90, height: 14, color: GOLD });
  page.drawText('1. VIBE CHECK', { x: margin, y: s1y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('Who is this for?', { x: margin, y: s1y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  const f1a = form.createTextField('vibe_who');
  f1a.addToPage(page, { x: margin, y: s1y - 60, width: midX - margin - 30, height: 22,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });

  page.drawText('What do they care about?', { x: margin, y: s1y - 78, size: 10, font: fontReg, color: DARK_GRAY });
  const f1b = form.createTextField('vibe_care');
  f1b.addToPage(page, { x: margin, y: s1y - 108, width: midX - margin - 30, height: 22,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });

  // --- SECTION 2: THE PROBLEM ---
  const s2y = contentTop - contentHeight / 2 - 4;
  page.drawRectangle({ x: margin - 2, y: s2y - 12, width: 95, height: 14, color: GOLD });
  page.drawText('2. THE PROBLEM', { x: margin, y: s2y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('What message/feeling?', { x: margin, y: s2y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  const f2 = form.createTextField('problem_message');
  f2.addToPage(page, { x: margin, y: s2y - 78, width: midX - margin - 30, height: 40,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });
  f2.enableMultiline();

  // --- SECTION 3: BRAINSTORM ---
  const s3x = midX;
  const s3y = contentTop - 4;
  page.drawRectangle({ x: s3x - 2, y: s3y - 12, width: 95, height: 14, color: GOLD });
  page.drawText('3. BRAINSTORM', { x: s3x, y: s3y - 10, size: 10, font: fontBold, color: NAVY });

  // Large sketch text field
  const sketchY = contentTop - contentHeight * 0.65 + 6;
  const sketchH = s3y - 20 - sketchY;
  const sketchW = width - margin - s3x;

  // Draw border for sketch area
  page.drawRectangle({ x: s3x, y: sketchY, width: sketchW, height: sketchH,
    borderColor: DOTTED_GRAY, borderWidth: 1, color: WHITE });

  const labelText = 'Type your brainstorm notes or ideas here';
  const ltw = fontItalic.widthOfTextAtSize(labelText, 9);
  page.drawText(labelText, { x: s3x + (sketchW - ltw) / 2, y: sketchY + 6,
    size: 9, font: fontItalic, color: DOTTED_GRAY });

  const f3 = form.createTextField('brainstorm');
  f3.addToPage(page, { x: s3x + 2, y: sketchY + 16, width: sketchW - 4, height: sketchH - 20,
    borderWidth: 0, backgroundColor: rgb(1, 1, 1) });
  f3.enableMultiline();

  // --- SECTION 4: BUILD IT ---
  const s4y = contentTop - contentHeight * 0.65 - 4;
  page.drawRectangle({ x: s3x - 2, y: s4y - 12, width: 72, height: 14, color: GOLD });
  page.drawText('4. BUILD IT', { x: s3x, y: s4y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('Tool:', { x: s3x, y: s4y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  const f4a = form.createTextField('build_tool');
  f4a.addToPage(page, { x: s3x + 32, y: s4y - 35, width: 128, height: 16,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });

  page.drawText('My prompt:', { x: s3x, y: s4y - 48, size: 10, font: fontReg, color: DARK_GRAY });
  const f4b = form.createTextField('build_prompt');
  f4b.addToPage(page, { x: s3x, y: s4y - 80, width: 160, height: 24,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });
  f4b.enableMultiline();

  // --- SECTION 5: DROP IT ---
  const s5x = s3x + 180;
  page.drawRectangle({ x: s5x - 2, y: s4y - 12, width: 68, height: 14, color: GOLD });
  page.drawText('5. DROP IT', { x: s5x, y: s4y - 10, size: 10, font: fontBold, color: NAVY });

  page.drawText('Feedback I got:', { x: s5x, y: s4y - 30, size: 10, font: fontReg, color: DARK_GRAY });
  const f5a = form.createTextField('drop_feedback');
  f5a.addToPage(page, { x: s5x, y: s4y - 50, width: width - margin - s5x, height: 16,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });

  page.drawText('One thing I\'d change:', { x: s5x, y: s4y - 60, size: 10, font: fontReg, color: DARK_GRAY });
  const f5b = form.createTextField('drop_change');
  f5b.addToPage(page, { x: s5x, y: s4y - 80, width: width - margin - s5x, height: 16,
    borderWidth: 1, borderColor: DOTTED_GRAY, backgroundColor: FIELD_BG });

  // === FOOTER BAR ===
  page.drawRectangle({ x: 0, y: 0, width, height: 36, color: NAVY });
  const footerText = '"Design with purpose. Create with AI."';
  const ftw = fontItalic.widthOfTextAtSize(footerText, 11);
  page.drawText(footerText, { x: (width - ftw) / 2, y: 13, size: 11, font: fontItalic, color: GOLD });

  const pdfBytes = await doc.save();
  const outPath = path.join(__dirname, 'Creator-Blueprint-Fillable.pdf');
  fs.writeFileSync(outPath, pdfBytes);
  console.log('Fillable handout saved to', outPath);
}

createFillable().catch(err => { console.error(err); process.exit(1); });
