# Network Roleplay: Pizza Shop

**A physical, unplugged simulation of how data travels across the internet**

> Part of the [Ready · Remix · Run](https://github.com/Ready-Remix-Run) archive of classroom-tested CS assignments.

---

## At a Glance

| | |
|---|---|
| **Author** | Tammy Pirmann, Drexel University |
| **Assignment Type** | Unplugged / physical roleplay activity |
| **CS Concepts** | Networking, packet switching, routing, net neutrality, deep packet inspection |
| **Grade Band** | Middle school · High school |
| **Time Required** | 1 class period (50–60 min) |
| **Prerequisites** | None — this works well as a first introduction to networking |
| **Materials** | Yarn, scissors, paper (packet blanks), writing implements, optional paper clips and paper plates |

---

## Overview

Students become the internet. Physically.

In this roleplay activity, students take on the roles of clients, routers, and pizza shop servers in a human-scale network connected by strands of yarn. To place a pizza order, a client writes their message on paper, cuts it into strips (packets), and sends each one sliding down the yarn toward a router. Routers read the destination address on each packet and pass it along toward the pizza shop — which reassembles the packets, reads the order, and sends a confirmation back the same way.

The activity has two rounds. In the first, all routers are neutral — they move packets along without reading the contents. In the second, some routers are "biased": they peek inside packets and drop any that mention certain pizza toppings. This is the moment the discussion about net neutrality comes alive, because students have just experienced it firsthand.

This assignment was originally designed when net neutrality was in the news, and it remains one of the most effective ways to make an abstract policy debate feel immediate and personal.

---

## Learning Objectives

By the end of this assignment, students will be able to:

- Explain how data is broken into packets and reassembled at its destination
- Describe the role of routers in moving packets across a network
- Distinguish between neutral and biased routing behavior
- Articulate the real-world implications of net neutrality using their own experience as evidence
- Discuss tradeoffs between network efficiency, privacy, and fairness

---

## Files in This Folder

| File | Description |
|------|-------------|
| `README.docx` | Facilitator overview, supply list, setup hints, and discussion prompts |
| `SetUp.xlsx` | Network topology diagram showing how to arrange students and connect yarn wires |
| `PacketBlank.docx` | Printable packet template — students write messages on one side, address info on the other |
| `ClientInstructions.docx` | Role card for client computers (pizza orderers) |
| `PizzaShopInstructions.docx` | Role card for pizza shop servers |
| `NeutralRouterInstructions.docx` | Role card for neutral routers |
| `BiasedRouterInstructionsMeat.docx` | Role card for a biased router that drops packets containing meat toppings |
| `BiasedRouterInstructionsMushrooms.docx` | Role card for a biased router that drops packets containing mushrooms |
| `BiasedRouterInstructionsPeppers.docx` | Role card for a biased router that drops packets containing peppers |
| `preStudentSetUp.jpg` | Photo showing the physical network setup before students arrive |

---

## How to Teach It

### Before Class
- Review `SetUp.xlsx` to plan your room arrangement — chairs work well as "nodes," or students can simply stand in position
- Cut yarn into appropriate lengths to connect students in the network topology
- Print enough copies of each role card and packet blanks for your class
- Optional: prepare a printed pizza shop price list (students enjoy neighborhood-specific touches like local favorites)
- Optional: use paper plates as name signs for each role, and paper clips to keep packets from falling off the yarn in drafty rooms

### In Class
1. **Set the scene** (5 min) — Explain that everything on a computer — documents, images, music, pizza orders — is transmitted as data. Today they are going to be the network.
2. **Assign roles and explain the setup** (5–10 min) — Distribute role cards. Walk through how packets work: message on one side, addressing info on the other, cut into strips, sent one at a time.
3. **Round 1: Neutral network** (15–20 min) — All routers are neutral. Clients write and send pizza orders; pizza shops receive, reassemble, and respond. Let the chaos unfold naturally.
4. **Round 2: Biased routers** (10–15 min) — Swap in biased router cards without announcing what they do. Watch what happens to certain orders. Students will notice.
5. **Discussion** (10–15 min) — See discussion questions below. Do not skip this part — it's where the learning lands.

### Discussion Questions
- Did each packet take the same path to its destination? Does the system still work if packets take different paths?
- What happened when a packet got lost? How might a real network handle this?
- In round 2, some routers were reading the contents of packets. Did this change the speed of delivery? Did it improve service? Was it fair?
- Who should decide what a router is allowed to do with a packet?
- Can you think of real-world situations where this kind of filtering happens?

---

## Adapting for Different Audiences

### Make It Easier
- Pre-address packets for students so they can focus on the physical routing experience
- Use a smaller, simpler network topology (fewer nodes, shorter paths)
- Run only the neutral router round and save the biased router discussion for a follow-up lesson

### Make It Harder
- Introduce packet loss deliberately (have a router randomly "drop" packets) and ask students to design an acknowledgment system
- Have students design their own network topology before running the activity
- Ask students to research real net neutrality policies and connect them to what they experienced

### Running It with Younger Students
- Simplify the packet format — just destination and a short message, no packet numbering needed
- Focus the debrief on the basic concept (messages travel in pieces) rather than net neutrality
- The biased router round still works well with younger students, framed as "what if someone was blocking your messages?"

### Connections to Other Courses
- **Social Studies / Civics:** Net neutrality as a policy issue; who regulates the internet and how
- **Media Literacy:** Who controls the flow of information online and why it matters
- **Math:** Routing as a graph theory problem; shortest path concepts

---

## Classroom Notes

*This section is for real stories from teachers who have used this assignment. If you've taught Network Roleplay and want to contribute your experience — what worked, what surprised you, what you'd do differently — please open a pull request or an issue.*

---

## Credits & License

Created by **Tammy Pirmann**, Drexel University (drpirmann@gmail.com).

Shared under [Creative Commons Attribution Non-Commercial 4.0 (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). You are free to use and adapt this assignment for non-commercial purposes — please credit the original author.
