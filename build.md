# How to Build
1. Make sure you have pyarmor and pyinstaller installed. `pip install pyinstaller pyarmor`
2. `pyarmor pack --clean -e "--onefile " src/colossalcyberadventure/main.py`
3. Your exe is in `src/colossalcyberadventure/dist/main.exe`

Remember, when distributing the exe you also distribute the resources folder like this:
```
resources/
    *
main.exe
```
