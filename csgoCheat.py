import ctypes

import pymem
import pymem.process
import keyboard
from Utils.Offsets import *
import time

def main():
    # getting handle to csgo process
    try:
        pm = pymem.Pymem("csgo.exe")
    except Exception as e:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        quit(0)
    # getting client and engine dll modules as well as updating netvars
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    engine_pointer = pm.read_uint(engine + dwClientState)

    # Initialising Variable
    cham = False
    First = True

    print("DUMPING NETVARS")
    print("DUMPING OFFSETS SUCCESFUL")
    print("CHEAT STARTED")

    while True:
        if client and engine and pm:
            try:  # Getting variables
                player, engine_pointer, glow_manager, crosshairid, getcrosshairTarget, immunitygunganme, \
                    localTeam, crosshairTeam, y_angle = GetPlayerVars(pm, client, engine, engine_pointer)
            except Exception as e:
                print("Round not started yet")
                time.sleep(2)
                continue

        if keyboard.is_pressed("end"):
            exit(0)

        for i in range(0, 64):  # Looping through all entities
            entity = pm.read_uint(client + dwEntityList + i * 0x10)
            if entity:
                pm.write_int(entity + m_bSpotted, 1)


def GetPlayerVars(pm, client, engine, engine_pointer):
    player = pm.read_uint(client + dwLocalPlayer)
    engine_pointer = pm.read_uint(engine + dwClientState)
    glow_manager = pm.read_uint(client + dwGlowObjectManager)
    crosshairid = pm.read_uint(player + m_iCrosshairId)
    getcrosshairtarget = pm.read_uint(client + dwEntityList + (crosshairid - 1) * 0x10)
    immunitygunganme = pm.read_uint(getcrosshairtarget + m_bGunGameImmunity)
    localteam = pm.read_uint(player + m_iTeamNum)
    crosshairteam = pm.read_uint(getcrosshairtarget + m_iTeamNum)
    y_angle = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)

    return player, engine_pointer, glow_manager, crosshairid, getcrosshairtarget, immunitygunganme, localteam, \
        crosshairteam, y_angle



if __name__ == "__main__":
    main()
else:
    print("Program Is not allowed to be ran, by other programs!")
    quit(0)