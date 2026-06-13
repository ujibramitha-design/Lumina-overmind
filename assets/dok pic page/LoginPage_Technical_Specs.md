# Technical Documentation: Tactical Auth Page (LUMINA)

Dokumentasi ini menjelaskan spesifikasi desain dan teknis dari halaman login "Tactical UI" yang telah diimplementasikan.

## 🎨 Spesifikasi Desain (Branding)
- **Tema**: Tactical / Stealth Mode Enterprise.
- **Warna Utama**:
  - Background Halaman: `bg-black` (#000000)
  - Background Input: `bg-zinc-900` (#18181b)
  - Aksen/Highlight: `emerald-500` (#10b981)
  - Teks Utama (Soft): `zinc-300` (#d4d4d8)
  - Teks Redup (Placeholder): `zinc-700` (#3f3f46)
- **Tipografi**: Font Monospace (font-mono) untuk kesan terminal/sistem.

## 🛠️ Fitur Teknis Utama
1. **Animated Grid Background**:
   - Lapisan latar belakang menggunakan grid CSS dinamis dengan efek `pulse` (berdenyut) untuk memberikan kesan sistem yang sedang aktif.
   - Menggunakan gradien halus dan blur emerald di bagian tengah.

2. **Ultra-Aggressive Autofill Fix**:
   - Menggunakan teknik `box-shadow inset` dan `transition` durasi tinggi untuk mencegah browser (Chrome/Edge) mengubah warna kotak input menjadi putih saat menggunakan fitur "Remember Password".
   - Memaksa `color-scheme: dark` di level input.

3. **Subtle Neon Focus**:
   - Saat input diklik (fokus), terdapat perubahan border ke `emerald-500/30` yang sangat tipis agar tidak menyilaukan mata pengguna di lingkungan minim cahaya.

4. **Floating Particles**:
   - Efek partikel kecil yang bergerak secara acak di latar belakang untuk menambah kedalaman visual (depth).

## 📂 Struktur Komponen (Frontend)
- **App Shell**: Next.js App Router.
- **Library UI**: Shadcn/UI (Input, Card, Button).
- **Icons**: Lucide-React (Shield, Terminal, Eye, Alert).

---
*Dokumentasi ini dibuat secara otomatis oleh Lumina Overmind Agent untuk referensi pengembangan di masa depan.*
