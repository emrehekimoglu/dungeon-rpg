<h1 align="center">🎮 Dungeon RPG</h1>
<h3 align="center">Terminal Tabanlı RPG Oyunu | Python</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Game-RPG-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

---

## 🧾 Proje Hakkında

Dungeon RPG, Python ile geliştirilmiş **terminal tabanlı bir rol yapma oyunudur (RPG)**.  
Oyuncu, seçtiği karakter sınıfı ile düşmanlara karşı savaşır, loot toplar ve seviye atlayarak ilerler.

Bu proje, oyun geliştirme süreçlerinde kullanılan **core game system** mantıklarını anlamak ve uygulamak amacıyla geliştirilmiştir.

---

## ⚔️ Oynanış

Oyuncu:

- 🧙‍♂️ Karakter sınıfı seçer  
- 👾 Rastgele oluşturulan düşmanlarla savaşır  
- 🎒 Loot toplar ve güçlenir  
- 📈 Deneyim kazanarak level atlar  
- ⚠️ Zorluk seviyesi giderek artan bir dünyada hayatta kalmaya çalışır  

---

## 🧩 Özellikler

- 🎮 **3 farklı karakter sınıfı**
  - Warrior  
  - Rogue  
  - Wizard  

- ⚔️ **Combat sistemi**
  - Normal Attack  
  - Strong Attack  
  - Heal  

- 📈 **Level & Experience sistemi**

- 🎒 **Loot sistemi**
  - Sword, Shield, Potion, Scroll  

- 🧠 **RPG Stat sistemi**
  - STR, DEX, CON, INT, WIS, CHA  

- 👾 **Procedural enemy generation**
  - Generator kullanımı ile dinamik düşman üretimi  

- 🧩 **Event sistemi**
  - Blacksmith event  

---

## 🧠 Teknik Detaylar

Bu proje aşağıdaki yazılım konseptlerini içermektedir:

- Object-Oriented Programming (OOP)
- Decorator kullanımı (`combat`)
- Generator fonksiyon (`enemy_spawner`)
- State management (HP, mana, level)
- Random event & loot sistemi  

---

## 🎮 Game Systems Perspektifi

Bu projede geliştirilen mekanikler, modern oyunlardaki temel sistemlerle benzerlik göstermektedir:

- Combat loop  
- Progression sistemi (leveling & experience)  
- Loot & reward mekanikleri  
- Event-driven gameplay  

Bu yapı, özellikle oyun backend sistemleri ve gameplay logic açısından temel bir örnek oluşturur.

---

## ▶️ Kurulum & Çalıştırma

```bash
git clone https://github.com/emrehekimoglu/dungeon-rpg
cd dungeon-rpg
python main.py
