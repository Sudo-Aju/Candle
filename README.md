# Candle - Birthday Card YSWS Project

> blow out the candle. make a wish. dont sneeze on your keyboard.

A birthday-themed python program where you literally **blow into your mic** (it wont extingiuis even i f you shout out loud, to know how that works refer to "how it works" section) to extinguish a candle. built with pygame, real-time audio processing, a custom perlin noise particle system, and way too much love.

---

## What it does

the flame reacts to how hard you blow in real time, particles move with organic perlin-style noise so it looks actually alive. when you blow hard enough the candle goes out with a poof of smoke, confetti explodes everywhere, and you can relight it and do it again. you can also tweak the mic sensitivity and screen size in `settings.json` if the blowing aint registering right.

---

## Download for Windows (no Python needed!)

grab the latest `BirthdayCandle.exe` from the [Releases page](../../releases/latest), unzip and run.

windows might show a security warning since the exe isnt signed, just click "more info" then "run anyway".

---

## Run from source (Mac / Linux / Windows)

clone the repo and install the dependencies:

```bash
pip install pygame pyaudio numpy
```

on windows if pyaudio fails to install do this instead:

```bash
pip install pipwin
pipwin install pyaudio
```

then just run:

```bash
python main.py
```

press space to light the candle, blow into your mic to extinguish it, and press R to relight.

---

## How it works

**audio** - uses pyaudio to read raw mic input at 44100hz, calculates the RMS amplitude of each chunk, smooths it over a rolling window of 10 frames and converts it to a blow intensity float that drives everything else.

**particles** - theres two particle types, fire and smoke. fire particles rise with randomized velocity and shift color from yellow to orange to red as they age. smoke particles expand in radius over time and fade out with alpha transparency. both get pushed sideways based on blow intensity.

**perlin noise** - custom 1D perlin-style noise using a permutation table. the wick and particles both sample noise based on time and position so the flame wobbles organically instead of looking robotic.

**confetti** - spawns a bunch of confetti pieces above the screen that fall with sine-wave drift and rotation, cleans itself up once everything falls off screen.

**config** - loads and saves a `settings.json` where you can change the mic threshold, blow limit, screen size and fps.

---

made with love for a bday buddy