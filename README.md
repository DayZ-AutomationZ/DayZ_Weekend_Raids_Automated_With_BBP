# DayZ_Weekend_Raids_Automated_With_BBP
DayZ raid-mode switcher for Nitrado: a Raspberry Pi script that uploads raid-ON / raid-OFF cfggameplay.json via FTP. Automatically toggles disableBaseDamage and disableContainerDamage on a schedule (e.g. weekend raids) using cron. No extra DayZ mods required. Optional BaseBuildingPlus files. can be ignored. it will still work.

# Automatic Weekend Raids Mode (cfgGameplay switcher + optional BaseBuildingPlus switcher)

This package lets you toggle **raiding on/off** from a Raspberry Pi (or any machine with Python)
by uploading different config files to your DayZ server via FTP. 
NO NEED FOR MODS!! Simple ftp uploads via PI VPS or whatever you want to use running python Can even do it on your android!

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

Put all these files on your Pi in e.g. `/home/PIusername/dayz_raid`:

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
cd /home/PIusername/dayz_raid

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

On the Pi, edit cron: (Change PIusername!) adjust times to your server restart times. make sure the files are uploaded at least a few minutes before restarts.

```bash
crontab -e
```

```cron

# --- RAID OFF BEFORE ALL RESTARTS (EVERY DAY) ---
0 0 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off
5 6 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off
5 12 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off
5 18 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off

# --- RAID OFF AT END OF RAID WINDOW (23:59 FRI/SAT/SUN) ---
59 23 * * 5 python3 /home/PIusername/dayz_raid/raid_mode.py off
59 23 * * 6 python3 /home/PIusername/dayz_raid/raid_mode.py off
59 23 * * 0 python3 /home/PIusername/dayz_raid/raid_mode.py off

# --- RAID ON AT 18:00 (FRI/SAT/SUN) ---
0 18 * * 5 python3 /home/PIusername/dayz_raid/raid_mode.py on
0 18 * * 6 python3 /home/PIusername/dayz_raid/raid_mode.py on
0 18 * * 0 python3 /home/PIusername/dayz_raid/raid_mode.py on
```

- Times are server local time MAKE SURE THE PI or VPS or any machine you run this on has same server time setting as your server.
- Always restart the DayZ server **after** a config upload for it to take effect.

---

Have fun raiding only when **Your server** says it’s time. 🦌🔨 YOU NEED TO SET UP THE TIME CORRECT WITH YOUR SERVER RESTARTS. 

The server used for this code had the following server restarts. 
Make Sure to set the time on the PI or whatever server you use the same as your game server

game_server_restart	Time: 00:06
Last Run: 09-12-2025 00:06:14 UTC +01:00
Next Run: 10-12-2025 00:06:00 UTC +01:00	Automated server restart in progress...	
game_server_restart	Time: 06:09
Last Run: 08-12-2025 06:10:04 UTC +01:00
Next Run: 09-12-2025 06:09:00 UTC +01:00	Automated server restart in progress...	
game_server_restart	Time: 12:09
Last Run: 08-12-2025 12:09:43 UTC +01:00
Next Run: 09-12-2025 12:09:00 UTC +01:00	Automated server restart in progress...	
game_server_restart	Time: 18:08
Last Run: 08-12-2025 18:08:20 UTC +01:00
Next Run: 09-12-2025 18:08:00 UTC +01:00	Automated server restart in progress...


## 6. Notes

- If you **don’t** use BBP:
  - Just ignore the BBP JSON files.
  - `raid_mode.py` will print a warning and move on if the BBP folder doesn’t exist.

- If Nitrado (or another host) UI overwrites cfgGameplay.json on restart:
  - Make sure you enable **Expert Mode** and **stop using the panel sliders** for base damage.
  - Your Pi + cron is now the boss for raid times.
