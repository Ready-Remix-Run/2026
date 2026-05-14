# Crayon Commotion

**A collaborative, unplugged activity that reveals how computers store images as numbers**

> Part of the [Ready · Remix · Run](https://github.com/Ready-Remix-Run) archive of classroom-tested CS assignments.

---

## At a Glance

| | |
|---|---|
| **Author** | Jeffrey L. Popyack, Drexel University |
| **Assignment Type** | Unplugged / hands-on group activity |
| **CS Concepts** | Digital image representation, color tables, data encoding, GIF format, pixels |
| **Grade Band** | Elementary · Middle school · High school |
| **Time Required** | 1 class period (50–60 min) |
| **Prerequisites** | None — accessible to any age group |
| **Materials** | Easel pad (25" × 30"), crayons, printed mini-pages, tape or paper clips |

---

## Overview

Students collaboratively recreate a pixelated image using crayons and a number-based color system — without knowing what the final picture will be until the very end.

Each student receives one or more "mini-pages": small 4×3 grids filled with numbers. A posted color table tells them which crayon color corresponds to each number. Students color in their grids and attach the completed mini-pages to a large easel in their assigned positions. As the mini-pages accumulate, a pixel-art image gradually emerges — and the big reveal never gets old.

The activity makes visceral and memorable something that is otherwise purely abstract: the idea that every image on a computer is simply a table of numbers. No binary required. No devices required. Just crayons, paper, and a room full of people working together toward something they can't quite see yet.

The activity scales beautifully — from a kindergarten classroom focusing purely on the "numbers become pictures" idea, to a high school CS class connecting the activity to GIF encoding, color depth, and compression tradeoffs.

---

## Learning Objectives

By the end of this activity, students will be able to:

- Explain that digital images are stored as tables of numbers
- Describe how a color table maps numbers to colors
- Define what a pixel is and how pixels combine to form an image
- Connect the activity to real file formats (GIF and beyond)
- Appreciate why standardized encoding matters for sharing data across systems

---

## Files in This Folder

| File | Description |
|------|-------------|
| `Crayon_Commotion_Instructions.pdf` | Full facilitator setup and implementation guide |
| *(image-specific files)* | Mini-pages, color tables, color maps, and data sheets are generated per image — see setup instructions |

> **Note:** The image-specific files (mini-pages, color tables, etc.) are generated using a Python workflow described in the setup instructions. The repo includes the tools needed to generate these for any image you choose.

---

## How to Teach It

### Before Class (Allow extra lead time — setup is involved)
- Select your image and generate the mini-pages, color table, color map, and data sheet using the provided tools
- Print mini-pages and verify cell size is approximately 0.75"–0.80" per square (use print scaling if needed); there are 6 mini-page grids per printed page
- Cut out mini-pages along the top and left edges only — leave the bottom and right margins intact, as they serve as guides for alignment and carry the page labels (e.g., A-1)
- Draw a labeled grid on the easel pad matching the mini-page dimensions: 8 columns (A–H) × 12 rows (1–12) = 96 mini-pages total
- Sort crayons into numbered bags or containers matching the color table
- Print the color table for prominent display; print the color map and data sheet as facilitator-only cheat sheets
- Optional: prepare a few blank mini-pages as replacements in case of coloring errors

### In Class
1. **Introduce the concept** (5–10 min) — Explain that all information on a computer, including images, is stored as numbers. Today's activity shows exactly how that works for images. Introduce the color table and the mini-page format.
2. **Distribute mini-pages and get coloring** (25–30 min) — Hand out mini-pages. Students find their assigned colors using the color table and fill in each cell. As they finish, they attach their mini-pages to the easel in the labeled position.
3. **The reveal** (5 min) — Step back and let students see the completed image emerge. This moment lands every time.
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
- Assign mini-pages to small teams rather than individuals
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

Created by **Jeffrey L. Popyack**, Drexel University (popyack@drexel.edu).

Shared under [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to use, adapt, and share this assignment — please credit the original author.
