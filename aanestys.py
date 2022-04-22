# Implemented by Teuvo Eloranta 04/2022.

from os import system, stat, remove, path
from string import digits 
from time import sleep
import json
import sys


FILE = "arvot.json"

sVals = ""
vals = []

system("cls")


def storeValues():
    """
    Save the the asked values
    into the JSON file.
    """
    global vals

    prevExists = True if path.exists(FILE) else False

    name = input("\n Anna nimi lukujoukolle: ")

    if not prevExists:
        _d = {}
        _d[name] = vals
    else:
        with open('arvot.json', "r") as f:
            _d = json.load(f)
            _d[name] = vals

    with open(FILE, "w") as f:
        f.write(json.dumps(_d))


def aver():
    """
    Calculate average from the values
    and show it in screen.
    """

    global vals

    system("cls")
    print("\n Keskiarvo: {:.2f} / {} lukua.".format(sum(vals)/len(vals), len(vals)))


def showSaved():
    """
    Show all the saved value sets
    stored in JSON file.
    """

    if not path.exists(FILE):
        print("\n Vanhoja lukujoukkoja ei löytynyt.\n")
    else:
        print("\n Talletetut lukujoukot:")
        print(" ----------------------")

        with open('arvot.json', "r") as f:
            _d = json.load(f)

        for key in _d:
            vals = str(_d[key]).replace("[", "").replace("]", "")
            print("\n {:20} k-a: {:.2f}   ({})".format(key, sum(_d[key])/len(_d[key]), vals) )
        print("\n\n")

    sys.exit(0)


def removeOne():
    """
    Remove a selected set of values
    from JSON file.
    """

    with open('arvot.json', "r") as f:
        _d = json.load(f)

    _lst = []

    print("\n Lukujoukot:\n")

    for i, key in enumerate(_d):
        print(" " + str(i+1) + ") " + key)
        _lst.append(key)

    ind = int(input("\n Valitse poistettava lukujoukko sen numerolla: ")) - 1

    if input("\n Poistetaanko '%s' varmasti? K/E: " % _lst[ind]).lower() == "k":
        _d.pop(_lst[ind], None)
        print("\n -> poistettu\n")

    with open(FILE, "w") as f:
        f.write(json.dumps(_d))

    sys.exit(0)


def info():
    """
    Show description of the program.
    """

    print("""\n
 Ohjelma kerää lukuarvoja käyttäjältä yksi kerrallaan ja lopulta 
 tallettaa ne tiedostoon arvot.json käyttäjän valitsemalla nimellä.
 Ohjelma näyttää annettujen arvojen keskiarvon.

 Ohjelmaa voi käyttää vaikka "levyraadissa" - käyttäjien kappaleelle 
 antamat arvot kysellään ohjelmaan ja lopulta ne talletetaan kappaleen
 nimellä talteen. Lopuksi kaikki talletetut äänet luetaan ohjelmalla
 tiedostosta ja katsotaan mikä sai parhaat pisteet.
 \n
 Ohjelman versio: 0.1  (23.04.2022)
 \n""")

    sys.exit(0)


def delOldValues():
  """
  Ask if old values are removed
  form JSON file before string new ones.
  """

  if not path.isfile(FILE):
      return

  if stat(FILE).st_size > 0:
      if input("\n Poistetaanko aiemmin talletetut vanhat arvot ensin? K/E: ").lower().startswith("k"):
          sleep(1.6)
          if input("\n Oletko varma? K/E: ").lower() == "k":
              remove(FILE)
              print("\n -> Vanhat arvot poistettu.")


def askNewValues():
  """
  Ask values from the user
  and save them in the end.
  """

  while True:
      print("\n Kirjoita 'e' lopettaaksesi arvojen syötön.\n")

      val = input("\n Anna luku: ")

      if val == "":
          continue
      elif val.startswith("e"):
          break
      elif val[0] in digits:
          vals.append(float(val))
      else:
          continue

      aver()

  if vals:
      aver()
      storeValues()

  sys.exit(0)


def main():
  """
  Ask what is done from the user
  """

  print("\n Valitse toimenpide 1-4:\n")
  print(" 1) Anna uusi lukujoukko")
  print(" 2) Näytä talletetut lukujoukot")
  print(" 3) Poista tallennettu lukujoukko")
  print(" 4) Näytä ohje")

  action = input("\n Valintasi: ")

  if action == "2":
      showSaved()

  elif action == "3":
      removeOne()

  elif action == "4" or "-h" in sys.argv or "-help" in sys.argv:
      info()


  delOldValues()

  askNewValues()


if __name__ == '__main__':
    main()