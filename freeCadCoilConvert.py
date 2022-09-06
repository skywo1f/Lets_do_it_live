from FreeCAD import Base
import Draft, Part
file = open("good2dCoil.csv")
wire = []
X=Y=Z = 0.0

for ligne in file:
    coordinates = ligne.split(",")
    try:                                                        # for format PCD ignore the header
        X,Y = coordinates                                     # separate the coordinates
        print(X," ",Y)
        wire.append(FreeCAD.Vector(float(X),float(Y))) # append the coordinates
    except Exception:
        None
file.close()
Draft.makeWire(wire,closed=False,face=False,support=None)   # create the wire open

App.ActiveDocument.recompute()
