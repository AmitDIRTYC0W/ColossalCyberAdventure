from subprocess import check_call
from glob import glob


def build():
    schemas = glob("submodules/ColossalCyberAdventureMessages/*.capnp")
    _ = check_call(["capnp", "compile", "-I", "submodules/ColossalCyberAdventureMessages",
                    "--output=pycapnp:src/colossalcberadventure", *schemas])


if __name__ == "__main__":
    build()
