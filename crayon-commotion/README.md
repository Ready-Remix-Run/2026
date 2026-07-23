# Crayon Commotion

**A collaborative, unplugged activity that reveals how computers store images as numbers**

> Part of the [Ready · Remix · Run](https://github.com/Ready-Remix-Run) archive of classroom-tested CS assignments.

---

## At a Glance

| | |
|---|---|
| **Authors** | Jeffrey L. Popyack, Drexel University revised by Tammy Pirmann, Drexel University |
| **Assignment Type** | Unplugged / hands-on group activity |
| **CS Concepts** | Digital image representation, color tables, data encoding, GIF format, pixels |
| **Grade Band** | Elementary · Middle school · High school · Community event|
| **Time Required** | 1 class period (50–60 min) depending on image size |
| **Prerequisites** | None — accessible to any age group |
| **Materials** | Easel pad (25" × 30"), crayons, printed mini-pages, tape |

---

## Overview

Students collaboratively recreate a pixelated image using crayons and a number-based color system — without knowing what the final picture will be until the very end.

Each student receives one or more "mini-pages": small grids filled with numbers. A posted color table tells them which crayon color corresponds to each number. Students color in their grids and attach the completed mini-pages to a large easel in their assigned positions. As the mini-pages accumulate, a pixel-art image gradually emerges — and the big reveal never gets old.

The activity makes visceral and memorable something that is otherwise purely abstract: the idea that every image on a computer is simply a table of numbers. No binary required. No devices required. Just crayons, paper, and a room full of people working together toward something they can't quite see yet.

The activity scales beautifully — from an elementary classroom focusing purely on the "numbers become pictures" idea, to a high school CS class connecting the activity to GIF encoding, color depth, and compression tradeoffs.

---

## Learning Objectives

By the end of this activity, students will be able to:

- Explain that digital images are stored as tables of numbers
- Describe how a color table maps numbers to colors
- Define what a pixel is and how pixels combine to form an image
- Connect the activity to real file formats (BMP, PNG and beyond)
- Appreciate why standardized encoding matters for sharing data across systems

---

## Files in This Folder

| File / Folder | Description |
|------|-------------|
| `Crayon Commotion Instructions.docx` | Original facilitator background and activity design notes |
| `generate_materials.ipynb` | Colab notebook — the easiest way to turn your own image into printable materials, no install required (see below) |
| `src/commotion/` | The Python package behind the notebook — image resizing, color quantization, and PDF generation. Written to be readable, not just runnable; browsable if you want to see how any step actually works |
| `palettes/crayola24.csv` | The default 24-color Crayola palette, as a plain `id,name,r,g,b` table |
| `palettes/crayola16.csv` | The standard 16-color Crayola box, for classrooms using the smaller pack |
| `images/` | Example source images used while building this tool |
| `output/` | Where generated PDFs/CSVs land when you run the tool locally |

---

## Generating Materials for a New Image

**Recommended: use the notebook, no installation needed.**

1. Open [`generate_materials.ipynb`](generate_materials.ipynb) in Colab: **[Open in Colab](https://colab.research.google.com/github/Ready-Remix-Run/2026/blob/main/crayon-commotion/generate_materials.ipynb)**
   
2. Upload your image when prompted.
3. Choose a palette (**Crayola 24** for more color accuracy, or **Crayola 16** if that's the box you have), your block size (how many pixels wide × tall each student's mini-page covers), and an encoding:
   - **Decimal** — a plain number per square (e.g. `18`). Simplest, works for any age.
   - **Binary** — a fixed-width binary number (e.g. `10010`). Participants decode it to decimal, then use the color reference chart, which stays decimal-keyed either way.
   - **RGB Binary** — three 8-bit binary numbers per square, one per red/green/blue component. Participants decode all three to a `R,G,B` decimal triple and match it directly on the reference chart, which switches to showing RGB values instead of palette ids. No lookup table involved — it's the actual color. The most advanced option, best for CS-teacher audiences.
   - **RGB Hex** — the same idea as RGB Binary, but each component is a 2-digit hex byte (e.g. `FF`, `A2`, `00`) instead of 8 binary digits. Shorter and quicker to decode than RGB Binary while still being the actual color; the reference chart shows the same RGB decimal triples either way.
4. Run the notebook. It downloads a zip containing:
   - A blank student sheet template, ready to print and duplicate
   - Encoding instructions for every mini-page (which numbers go where)
   - A large-format color reference chart, sized to hang on a wall
   - A teacher's cheat sheet showing the correct color for every square
5. Print, cut mini-pages along the top and left edges only, and you're ready — see *How to Teach It* below.

**For CS teachers who want to see or run the code directly:** the notebook is a thin wrapper around the `src/commotion/` package — nothing in it is hidden or notebook-only. To run it locally instead: `pip install -r requirements.txt`, then see `src/commotion/cli.py`, which walks through every pipeline step (image loading, resizing, color matching, splitting into mini-pages, PDF generation) against the sample images in `images/`.

Each printed mini-page cell is 1 cm square by default (0.5 cm on the teacher's cheat sheet, to keep color-printing costs down); both are configurable in the notebook.

---

## How to Teach It

### Before Class (Allow extra lead time — setup is involved)
- Generate your materials from *Generating Materials for a New Image* above: a blank student sheet, per-mini-page encoding instructions, a wall-sized color reference chart, and a teacher's cheat sheet
- Print blank student sheets and encoding instructions — each prints as many mini-page grids as comfortably fit per page (1 cm per square by default), so page count depends on your block size and image
- Cut out mini-pages along the top and left edges only — leave the bottom and right margins intact, as they serve as guides for alignment and carry the mini-page's position label (e.g., A-1)
- Draw a labeled grid on the easel pad matching the mini-page dimensions and the layout your generated materials use
- Sort crayons into numbered bags or containers matching the color reference chart
- Print the color reference chart for prominent display; print the teacher's cheat sheet as your facilitator-only answer key
- Optional: prepare a few blank mini-pages as replacements in case of coloring errors

### In Class
1. **Introduce the concept** (5–10 min) — Explain that all information on a computer, including images, is stored as numbers. Today's activity shows exactly how that works for images. Introduce the color table and the mini-page format.
2. **Distribute mini-pages and get coloring** (25–30 min) — Hand out mini-pages. Students find their assigned colors using the color table and fill in each cell. As they finish, they attach their mini-pages to the easel in the labeled position.
3. **The reveal** (5 min) — Step back and let students see the completed image emerge. Students generally enjoy and celebrate at this point.
4. **Debrief** (10–15 min) — See discussion questions below.

### Discussion Questions
- What would happen if the color table were different — say, if 3 meant blue instead of red?
- Why might a computer use numbers instead of just storing the color names directly?
- What are the limits of this system? How many colors could you represent?
- What happens if one mini-page has an error? How does that connect to data errors in real systems?
- Can you think of other things that computers store as numbers? (sound, video, text...)

---

## Adapting for Different Audiences

### For Elementary Students
- Use a simpler image with fewer colors and larger pixel grids
- Skip the GIF format discussion entirely — focus on "numbers become pictures"
- Frame it as a group art project with a mystery ending
- Consider assigning one mini-page per student or small group to reduce complexity

### For Middle School Students
- Introduce the vocabulary: pixel, color table, encoding, file format
- Ask students to predict what the image might be as mini-pages are added to the easel
- Connect to discussions of how images are shared and why file formats matter

### For High School Students
- Extend the discussion to color depth: how many bits are needed to represent N colors?
- Introduce compression: what if many adjacent pixels share the same color? How might you encode that more efficiently?
- Connect to real GIF, PNG, and JPEG encoding — and why different formats exist
- Have students research how lossless vs. lossy compression affects image quality

### Running It with Large Groups (Conferences, Assemblies)
- This activity was designed with large group settings in mind and works beautifully at events
- Assign mini-pages to small teams or individuals
- Have a few facilitators circulating to catch coloring errors early (use the cheat sheet)
- Consider running two images simultaneously — but note that color table numbering may differ between images, so use clearly distinct crayon sets for each

### Connections to Other Courses
- **Art:** Pixel art, pointillism, color theory
- **Math:** Coordinate systems (row/column addressing), number systems, combinatorics (how many colors with N bits?)
- **Science:** How the human eye perceives color; RGB vs. other color models

---

## Classroom Notes

*This section is for real stories from teachers who have used this assignment. If you've taught Crayon Commotion and want to contribute your experience — what worked, what surprised you, what you'd do differently — please open a pull request or an issue.*

---

## Credits & License

Original activity Created by **Jeffrey L. Popyack**, Drexel University (popyack@drexel.edu) as Post It Pandmonium.
This software enabled activity created by **Tammy Pirmann**, Drexel University (tammy.r.pirmann@drexel.edu).

Shared under [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to use, adapt, and share this assignment — please credit the original authors.
