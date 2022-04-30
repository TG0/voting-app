from os import system, stat, remove, path
from string import digits 
from time import sleep
import json
import sys
import signal
from numpy import arange
import matplotlib.pyplot as plt  # run 1st: pip3 install matplotlib


FILE = "data.json"

sVals = ""
vals = []



def sigHandler(signal, frame):
    """
    Exit nicely on CTRL+C
    """
    print("\n\n HEIPPA!\n\n")
    sys.exit(0)


signal.signal(signal.SIGINT, sigHandler)



def clearScreen():
    """
    """
    if sys.platform == "win32":
        system("cls")
    else:
        system("clear")


def pressToContinue():
    """
    press any key to continue
    to main view
    """
    input(" Paina jotain nappulaa jatkaaksesi: ")


def storeValues():
    """
    Save the the asked values
    into the JSON file.
    """
    global vals

    name = input("\n Anna nimi lukujoukolle: ")

    if not path.exists(FILE):
        _d = {}
        _d[name] = vals
    else:
        with open(FILE, "r") as f:
            _d = json.load(f)
            _d[name] = vals

    with open(FILE, "w") as f:
        f.write(json.dumps(_d))

    print("\n\n")


def avg(lst):
    """
    Returns average value of lst
    """
    return sum(lst) / len(lst)


def aver():
    """
    Calculate average from the values
    and show it in screen.
    """
    global vals

    clearScreen()
    print("\n Keskiarvo: {:.2f} / {} lukua.".format(avg(vals), len(vals)))


def oldValuesExist():
    """
    Exit operation nicely, if no old
    value sets in JSON file.
    """
    if not path.isfile(FILE):
        print("\n Vanhoja lukujoukkoja ei löytynyt.\n\n")
        pressToContinue()
        return False
    return True


def showBarPlot(names, values):
    """
    Generate and show bar plot.
    Show 5 biggest averages only.
    """
    for ind in range(len(names)):
        names[ind] += "\n" + str(values[ind])

    yPos = arange(len(names[:5]))
    plt.figure(figsize=(11, 6))
    plt.bar(yPos, values[:5], color='royalblue', alpha=0.7)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.6)
    plt.xticks(yPos, names[:5])
    plt.show()


def showSaved():
    """
    Show all the saved value sets
    stored in JSON file.
    Shows ordered by biggest to lowest average value calculated.
    """
    if not oldValuesExist():
        return

    clearScreen()

    print("\n Talletetut lukujoukot:")
    print(" ----------------------")

    with open(FILE, "r") as f:
        _d = json.load(f)

    # _d  = {KEY:LIST-OF-VALUES, ...}
    # _d2 = {AVG-VAL : KEY, ...}
    # _keys = [5, 4.2, 3,3, 2, 1.1, 0.4]

    _d2 = {}
    for key in _d:
        _d2[avg(_d[key])] = key

    _keys = sorted(_d2, reverse=True)

    _names = []
    _values = []

    for key in _keys:
        averVal = round(avg(_d[_d2[key]]), 2)
        vals = str(_d[_d2[key]]).replace("[", "").replace("]", "")
        
        print("\n {:20} k-a: {:4.2f}   ({})".format(_d2[key], averVal, vals))

        _names.append(_d2[key])
        _values.append(round(avg(_d[_d2[key]]), 2))

    print("\n\n")

    if input(" Näytä pylväsdiagrammi? K/E: ").lower() == "k":
        return showBarPlot(_names, _values)
    else:
      pressToContinue()



def removeValueSet():
    """
    Remove a selected set of values
    from JSON file.
    """
    oldValuesExist()

    with open(FILE, "r") as f:
        _d = json.load(f)

    _lst = []

    print("\n Lukujoukot:\n")

    for i, key in enumerate(_d):
        print(" " + str(i+1) + ") " + key)
        _lst.append(key)
    print(" x) poista kaikki")

    sel = input("\n Valitse poistettava lukujoukko sen numerolla (tai: x): ")

    if sel.lower() == "x":
        delOldValues()
    else:
        ind = int(sel) - 1

        if input("\n Poistetaanko '%s' varmasti? K/E: " % _lst[ind]).lower() == "k":
            if len(_d) == 1:
                remove(FILE)
            else:
                _d.pop(_lst[ind], None)

                with open(FILE, "w") as f:
                    f.write(json.dumps(_d))

            print("\n -> poistettu\n")
            pressToContinue()



def info():
    """
    Show description of the program.
    """
    print("""\n
 Ohjelma kerää lukuarvoja käyttäjältä yksi kerrallaan ja lopulta 
 tallettaa ne tiedostoon %s käyttäjän valitsemalla nimellä.
 Ohjelma näyttää annettujen arvojen keskiarvon ja piirtää näistä
 halutessa pylväsdiagrammin, jossa 5 suurinta keskiarvoa.

 Ohjelmaa voi käyttää vaikka "levyraadissa" - käyttäjien kappaleelle 
 antamat arvot kysellään ohjelmaan ja lopulta ne talletetaan kappaleen
 nimellä talteen. Lopuksi kaikki talletetut äänet luetaan ohjelmalla
 tiedostosta ja katsotaan mikä sai parhaat pisteet.
 \n
 Ohjelman versio: 0.3  (30.04.2022)
 \n""" % FILE)

    pressToContinue()


def delOldValues():
  """
  Ask if old values are removed
  form JSON file before string new ones.
  """
  oldValuesExist()

  if stat(FILE).st_size > 0:
      if input("\n Poistetaanko kaikki aiemmin talletetut lukujoukot? K/E: ").lower().startswith("k"):
          if input("\n Oletko varma? K/E: ").lower() == "k":
              remove(FILE)
              print("\n -> Vanhat arvot poistettu.")
              pressToContinue()


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
      del vals[:]


def main():
  """
  Ask the user what is done
  """
  while True:

      clearScreen()

      print("\n Valitse toimenpide 1-4:\n")
      print(" 1) Anna uusi lukujoukko")
      print(" 2) Näytä talletetut lukujoukot")
      print(" 3) Poista tallennettu lukujoukko")
      print(" 4) Näytä ohje")
      print(" e) Lopeta ohjelma")

      action = input("\n Valintasi: ")

      if action == "e":
        print("\n HEIPPA!\n\n")
        sys.exit(0)

      elif action == "2":
          showSaved()

      elif action == "3":
          removeValueSet()

      elif action == "4" or "-h" in sys.argv or "-help" in sys.argv:
          info()

      elif action == "1":
          askNewValues()

      else:
        continue


if __name__ == '__main__':
    main()


