# PARKING LOT MANAGEMENT SYSTEM SCRIPT

## Problem Statement

Design and implement a Parking Lot Management System that:

- Allocates slots to vehicles based on type and availability.
- Tracks vehicle entry, parking, and exit.
- Calculates parking duration and fees.
- Enforces parking rules (e.g., rejecting entry if no slot is available).

---

## Core Features

### Parking Lot & Slots

- Multi-level parking 
- Slot types:
  - `Regular` – Standard vehicles
  - `Electric` – EVs (with charging)
  - `Handicapped` – Accessible (near entrances)

### Vehicle Handling

- Vehicles defined by `license plate` and `type`.
- Entry checks slot availability and assigns appropriately.
- Rejection if no suitable slot is available.

### Tickets & Exit

- On exit, the system:
  - Retrieves ticket
  - Calculates parking duration
  - Computes fee and processes payment
  - Frees up the slot

---

## Bonus Features

- Reservations for future parking
- Waitlist when lot is full
- Fines for exceeding max parking duration

---
- version 1 -> what I coded during the coding round
- version 2 -> improved version with better object orientation
