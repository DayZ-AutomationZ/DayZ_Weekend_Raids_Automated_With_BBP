# DayZ Raid Mode Switcher (cfgGameplay + BBP)

This package lets you toggle **raiding on/off** from a Raspberry Pi (or any machine with Python)
by uploading different config files to your DayZ server via FTP.

It controls:
- `cfggameplay.json`  → vanilla bases / containers (disableBaseDamage, disableContainerDamage)
- `BBP_Settings.json` → BaseBuildingPlus structures (BBP_DisableDestroy)

You trigger it with:
```bash
python3 raid_mode.py on
python3 raid_mode.py off
```

and your cron schedule decides **when** raids are allowed.

---

## 1. Files in this package

Put all these files on your Pi in e.g. `/home/d3nd4n/dayz_raid`:

- `raid_mode.py`
- `cfggameplay_raid_on.json`
- `cfggameplay_raid_off.json`
- `BBP_raid_on.json`
- `BBP_raid_off.json`
- `README_RAID_MODE.md` (this file)

> If you don't use BaseBuildingPlus, you can ignore the BBP files.

---

## 2. Adjust the templates to your server

### 2.1 cfgGameplay templates

Open:

- `cfggameplay_raid_on.json`
- `cfggameplay_raid_off.json`

and **copy your own cfgGameplay.json** into both, then only change:

- In `cfggameplay_raid_on.json`:
  ```json
  "disableBaseDamage": false,
  "disableContainerDamage": false
  ```
- In `cfggameplay_raid_off.json`:
  ```json
  "disableBaseDamage": true,
  "disableContainerDamage": true
  ```

Keep all your other settings (stamina, UI, map, etc.) exactly the same as on your server.

### 2.2 BBP templates (optional, only if you use BBP)

Open:

- `BBP_raid_on.json`
- `BBP_raid_off.json`

and copy your own `BBP_Settings.json` content into both files.  
Then make sure:

- In `BBP_raid_on.json`:
  ```json
  "BBP_DisableDestroy": 0
  ```
  → BBP bases can be raided during the raid window.

- In `BBP_raid_off.json`:
  ```json
  "BBP_DisableDestroy": 1
  ```
  → BBP bases cannot be destroyed outside the raid window.

Keep all other BBP values (build anywhere, cement mixers, raid times, etc.) the same as you like.

---

## 3. Configure raid_mode.py

Edit `raid_mode.py` and set:

```python
FTP_HOST = "YOUR_FTP_HOST"
FTP_USER = "YOUR_FTP_USERNAME"
FTP_PASS = "YOUR_FTP_PASSWORD"
```

And adjust the remote paths if your host uses different folders:

```python
REMOTE_DIR_GAMEPLAY = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus"
REMOTE_CFG_GAMEPLAY = "cfggameplay.json"

REMOTE_DIR_BBP = "/dayzstandalone/config/BaseBuildingPlus"
REMOTE_CFG_BBP = "BBP_Settings.json"
```

On Nitrado for Chernarus, this layout is correct:
- `cfggameplay.json` lives in `dayzstandalone/mpmissions/dayzOffline.chernarusplus`
- `BBP_Settings.json` lives in `dayzstandalone/config/BaseBuildingPlus`

---

## 4. Test manually

On the Pi, from the folder where `raid_mode.py` lives:

```bash
cd /home/d3nd4n/dayz_raid

# Switch raids OFF
python3 raid_mode.py off

# Then restart the DayZ server from the Nitrado panel
```

Join the server and check:
- You **cannot** damage vanilla fences/doors with tools.
- If you use BBP and BBP_raid_off.json was uploaded, BBP walls should also be indestructible.

Then test raids ON:

```bash
python3 raid_mode.py on
# restart server
```

Now:
- Vanilla fences/doors are raidable (depending on your cfgGameplay settings).
- BBP walls are raidable if `BBP_DisableDestroy` is 0 in the ON template.

---

## 5. Example cron schedule (Fri/Sat/Sun 18:00–00:00)

On the Pi, edit cron:

```bash
crontab -e
```

Example combined with your ClaimBot:

```cron
*/5 * * * * cd /home/d3nd4n/ClaimBot && /usr/bin/python3 sync_pending_claims.py >> /home/d3nd4n/ClaimBot/sync_log.txt 2>&1

# --- RAID OFF BEFORE ALL RESTARTS (EVERY DAY) ---
0 0 * * * python3 /home/d3nd4n/dayz_raid/raid_mode.py off
5 6 * * * python3 /home/d3nd4n/dayz_raid/raid_mode.py off
5 12 * * * python3 /home/d3nd4n/dayz_raid/raid_mode.py off
5 18 * * * python3 /home/d3nd4n/dayz_raid/raid_mode.py off

# --- RAID OFF AT END OF RAID WINDOW (23:59 FRI/SAT/SUN) ---
59 23 * * 5 python3 /home/d3nd4n/dayz_raid/raid_mode.py off
59 23 * * 6 python3 /home/d3nd4n/dayz_raid/raid_mode.py off
59 23 * * 0 python3 /home/d3nd4n/dayz_raid/raid_mode.py off

# --- RAID ON AT 18:00 (FRI/SAT/SUN) ---
0 18 * * 5 python3 /home/d3nd4n/dayz_raid/raid_mode.py on
0 18 * * 6 python3 /home/d3nd4n/dayz_raid/raid_mode.py on
0 18 * * 0 python3 /home/d3nd4n/dayz_raid/raid_mode.py on
```

- Times are server local time (your Pi uses Europe/Amsterdam now).
- Always restart the DayZ server **after** a config upload for it to take effect.

---

## 6. Notes

- If you **don’t** use BBP:
  - Just ignore the BBP JSON files.
  - `raid_mode.py` will print a warning and move on if the BBP folder doesn’t exist.

- If Nitrado (or another host) UI overwrites cfgGameplay.json on restart:
  - Make sure you enable **Expert Mode** and **stop using the panel sliders** for base damage.
  - Your Pi + cron is now the boss for raid times.

- This setup is perfect for sharing on GitHub:
  - Simple Python, no external libraries.
  - Only requires FTP access and cron.