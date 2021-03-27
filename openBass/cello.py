import numpy as np


songLength = 654
song = np.array([[0 , 3],[1 ,5 ],[3 ,4 ],[2 ,7 ],[3 ,4 ],[1 ,5 ],[3 ,4 ],[1 ,5 ],[0 ,3 ],[1 ,5 ],[3 ,4 ],[2 ,7 ],[3 ,4 ],[1 ,5 ],[3 ,4 ],[1 ,5 ],[0 ,3 ],[2 ,2 ],[3 ,5 ],[3 ,4 ],[3 ,5 ],[2 ,2 ],[3 ,5 ],[2 ,2 ],[0 ,3 ],[2 ,2 ],[3 ,5 ],[3 ,4 ],[3 ,5 ],[2 ,2 ],[3 ,5 ],[2 ,2 ], [0 ,3 ],[2 ,4 ],[3 ,5 ],[3 ,4 ],[3 ,5 ],[2 ,4 ],[3 ,5 ],[2 ,4 ],[0 ,3 ],[2 ,4 ],[3 ,5 ],[3 ,4 ],[3 ,5 ],[2 ,4 ],[3 ,5 ],[2 ,4 ],[0 ,3 ],[2 ,5 ],[3 ,4 ],[2 ,7 ],[3 ,4 ],[2 ,5 ],[3 ,4 ],[2 ,5 ],[0 ,3 ],[2 ,5 ],[3 ,4 ],[2 ,7 ],[3 ,4 ],[2 ,5 ],[3 ,4 ],[2 ,4 ], [0 ,3 ],[2 ,2 ],[3 ,4 ],[3 ,2 ],[3 ,4 ],[2 ,5 ],[2 ,4 ],[2 ,5 ],[2 ,2 ],[2 ,5 ],[2 ,4 ],[2 ,5 ],[1 ,2 ],[1 ,5 ],[1 ,4 ],[1 ,2 ],[1 ,4 ],[2 ,5 ],[3 ,2 ],[2 ,5 ],[3 ,2 ],[2 ,5 ],[3 ,2 ],[2 ,5 ],[1 ,4 ],[2 ,5 ],[3 ,2 ],[2 ,5 ],[3 ,2 ],[2 ,5 ],[3 ,2 ],[2 ,5 ], [2 ,4 ],[2 ,7 ],[3 ,7 ],[3 ,6 ],[3 ,7 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[1 ,5 ],[2 ,4 ],[1 ,7 ],[1 ,5 ],[0 ,0 ],[1 ,2 ],[2 ,5 ],[2 ,4 ],[2 ,5 ],[1 ,2 ],[2 ,5 ],[1 ,2 ],[0 ,0 ],[2 ,2 ],[2 ,5 ],[2 ,4 ],[2 ,5 ],[2 ,2 ],[2 ,5 ],[2 ,2 ],[0 ,0 ],[1 ,4 ],[1 ,5 ],[1 ,7 ],[1 ,5 ],[1 ,4 ],[0 ,7 ],[0 ,5 ],[2 ,5 ],[2 ,4 ],[1 ,7 ],[3 ,7 ],[3 ,7 ],[3 ,4 ],[2 ,7 ],[2 ,5 ],[2 ,4 ],[1 ,7 ],[1 ,5 ],[3 ,7 ],[2 ,7 ],[3 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[1 ,7 ],[2 ,4 ],[2 ,7 ],[2 ,5 ],[2 ,4 ],[1 ,7 ],[1 ,5 ], [2 ,6 ],[1 ,5 ],[1 ,8 ],[1 ,7 ],[1 ,8 ],[1 ,5 ],[2 ,6 ],[1 ,5 ],[3 ,4 ],[1 ,5 ],[1 ,8 ],[1 ,7 ],[1 ,8 ],[1 ,5 ],[2 ,6 ],[1 ,5 ],[1 ,3 ],[2 ,2 ],[3 ,2 ],[3 ,4 ],[3 ,5 ],[3 ,2 ],[2 ,2 ],[1 ,5 ],[1 ,3 ],[2 ,2 ],[3 ,2 ],[3 ,4 ],[3 ,5 ],[3 ,2 ],[2 ,4 ],[2 ,2 ],[1 ,6 ],[2 ,4 ],[1 ,6 ],[2 ,4 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[2 ,4 ],[1 ,6 ],[2 ,4 ],[1 ,6 ],[2 ,4 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[2 ,4 ],[2 ,5 ],[2 ,4 ],[1 ,7 ],[2 ,5 ],[2 ,4 ],[2 ,5 ],[2 ,7 ],[2 ,4 ],[2 ,5 ],[2 ,4 ],[1 ,7 ],[1 ,5 ],[1 ,3 ],[1 ,2 ],[0 ,5 ],[0 ,3 ],[0 ,2 ],[1 ,3 ],[1 ,5 ],[1 ,3 ],[1 ,5 ],[1 ,3 ],[1 ,5 ],[1 ,3 ],[0 ,2 ],[1 ,3 ],[1 ,5 ],[1 ,3 ],[1 ,5 ],[1 ,3 ],[1 ,5 ],[1 ,3 ],[0 ,3 ],[1 ,2 ],[2 ,3 ],[2 ,2 ],[2 ,3 ],[1 ,2 ],[2 ,3 ],[1 ,2 ],[0 ,3 ],[1 ,2 ],[2 ,3 ],[2 ,2 ],[2 ,3 ],[1 ,2 ],[2 ,3 ],[1 ,2 ], [0 ,3 ],[1 ,3 ],[2 ,2 ],[1 ,5 ],[2 ,2 ],[1 ,3 ],[2 ,2 ],[1 ,3 ],[0 ,3 ],[1 ,3 ],[2 ,2 ],[1 ,5 ],[2 ,2 ],[1 ,3 ],[2 ,2 ],[1 ,3 ],[0 ,3 ],[2 ,4 ],[3 ,5 ],[3 ,4 ],[3 ,5 ],[2 ,4 ],[3 ,5 ],[2 ,4 ],[0 ,3 ],[2 ,4 ],[3 ,5 ],[3 ,4 ],[3 ,5 ],[2 ,4 ],[3 ,5 ],[2 ,4 ],[0 ,3 ],[1 ,5 ],[3 ,4 ],[3 ,2 ],[3 ,4 ],[2 ,5 ],[2 ,4 ],[2 ,2 ],[1 ,5 ],[1 ,3 ],[1 ,2 ],[0 ,5 ],[0 ,3 ],[0 ,2 ],[1 ,0 ],[1 ,5 ],[1 ,4 ],[0 ,5 ],[1 ,7 ],[2 ,4 ],[2 ,5 ],[1 ,7 ],[2 ,4 ],[2 ,5 ],[1 ,4 ],[0 ,5 ],[1 ,7 ],[2 ,4 ],[2 ,5 ],[1 ,7 ],[2 ,4 ],[2 ,5 ],[1 ,3 ],[0 ,5 ],[1 ,5 ],[2 ,2 ],[2 ,4 ],[1 ,5 ],[2 ,2 ],[2 ,4 ],[1 ,3 ],[0 ,5 ],[1 ,5 ],[2 ,2 ],[2 ,4 ],[1 ,5 ],[2 ,2 ],[2 ,4 ],[1 ,3 ],[0 ,5 ],[1 ,5 ],[2 ,4 ],[2 ,7 ],[3 ,6 ],[3 ,7 ],[0 ,5 ],[1 ,2 ],[1 ,3 ],[1 ,5 ],[2 ,2 ],[2 ,4 ],[2 ,5 ],[3 ,2 ],[2 ,4 ],[1 ,5 ],[2 ,2 ],[2 ,4 ],[2 ,5 ],[3 ,2 ],[3 ,4 ],[3 ,5 ],[3 ,2 ],[2 ,4 ],[2 ,5 ],[2 ,7 ],[3 ,4 ],[3 ,5 ],[3 ,7 ],[3 ,8 ],[3 ,7 ],[3 ,6 ],[3 ,7 ],[3 ,7 ],[3 ,5 ],[3 ,4 ],[3 ,5 ],[3 ,5 ],[2 ,7 ],[2 ,4 ],[1 ,7 ],[1 ,5 ],[1 ,0 ],[1 ,2 ],[1 ,3 ],[1 ,5 ],[0 ,5 ],[1 ,5 ],[2 ,4 ],[3 ,2 ],[3 ,4 ],[3 ,5 ],[3 ,2 ],[3 ,4 ],[2 ,5 ],[1 ,5 ],[1 ,3 ],[1 ,2 ],[0 ,3 ],[0 ,5 ],[1 ,2 ],[1 ,5 ],[0 ,3 ],[1 ,2 ],[1 ,5 ],[2 ,5 ],[3 ,2 ],[3 ,4 ],[2 ,5 ],[3 ,6 ],[3 ,4 ],[2 ,7 ],[2 ,8 ],[2 ,8 ],[2 ,7 ],[2 ,6 ],[2 ,7 ],[2 ,7 ],[2 ,5 ],[2 ,4 ],[2 ,5 ],[2 ,5 ],[1 ,7 ],[1 ,4 ],[0 ,7 ],[0 ,5 ],[1 ,4 ],[1 ,7 ],[2 ,5 ],[2 ,7 ],[3 ,6 ],[3 ,7 ],[3 ,6 ],[3 ,7 ],[2 ,7 ],[2 ,4 ],[1 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[2 ,4 ],[0 ,5 ],[1 ,5 ],[1 ,4 ],[0 ,7 ],[0 ,5 ],[0 ,3 ],[0 ,2 ],[0 ,0 ],[1 ,5 ],[3 ,5 ],[3 ,4 ],[3 ,2 ],[2 ,5 ],[2 ,4 ],[2 ,2 ],[1 ,5 ],[3 ,5 ],[3 ,4 ],[3 ,2 ],[2 ,5 ],[2 ,4 ],[2 ,2 ],[1 ,5 ],[1 ,3 ],[3 ,4 ],[3 ,2 ],[2 ,5 ],[2 ,4 ],[2 ,2 ],[1 ,5 ],[1 ,3 ],[1 ,2 ],[3 ,2 ],[2 ,5 ],[2 ,4 ],[2 ,2 ],[1 ,5 ],[1 ,3 ],[1 ,2 ], [0 ,5 ],[2 ,5 ],[2 ,4 ],[1 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[2 ,7 ],[1 ,7 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[2 ,7 ],[1 ,7 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[1 ,7 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[1 ,7 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[2 ,7 ],[1 ,7 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[2 ,7 ],[2 ,7 ],[3 ,4 ],[2 ,7 ],[1 ,5 ],[2 ,7 ],[2 ,7 ],[2 ,7 ],[3 ,4 ],[2 ,7 ],[3 ,5 ],[2 ,7 ],[1 ,5 ],[2 ,7 ],[3 ,4 ],[2 ,7 ],[3 ,5 ],[2 ,7 ],[3 ,7 ],[2 ,7 ],[3 ,4 ],[2 ,7 ], [3 ,5 ],[2 ,7 ],[3 ,4 ],[2 ,7 ],[3 ,5 ],[2 ,7 ],[2 ,7 ],[2 ,7 ],[3 ,4 ],[2 ,7 ],[2 ,7 ],[2 ,7 ],[3 ,4 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[2 ,7 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[2 ,7 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[2 ,5 ],[2 ,7 ],[1 ,7 ],[2 ,7 ],[2 ,4 ],[2 ,7 ],[1 ,5 ],[1 ,7 ],[2 ,3 ],[1 ,5 ],[2 ,4 ],[1 ,5 ],[2 ,5 ],[1 ,5 ],[2 ,6 ],[1 ,5 ],[2 ,7 ],[1 ,5 ],[2 ,8 ],[1 ,5 ],[3 ,4 ],[2 ,0 ],[3 ,5 ],[2 ,0 ],[3 ,6 ],[2 ,0 ],[3 ,7 ],[2 ,0 ],[3 ,8 ],[2 ,0 ],[3 ,9 ],[2 ,0 ],[3 ,10 ],[2 ,0 ],[3 ,11 ],[2 ,0 ], [3 ,12 ],[2 ,9 ],[0 ,10 ],[2 ,9 ],[3 ,12 ],[2 ,9 ],[3 ,12 ],[2 ,9 ],[3 ,12 ],[2 ,9 ],[0 ,10 ],[2 ,9 ],[3 ,12 ],[2 ,9 ],[3 ,12 ],[2 ,9 ], [3 ,12 ],[1 ,12 ],[0 ,10 ],[1 ,12 ],[3 ,12 ],[1 ,12 ],[3 ,12 ],[1 ,12 ],[3 ,12 ],[1 ,12 ],[0 ,10 ],[1 ,12 ],[3 ,12 ],[1 ,12 ],[3 ,12 ],[1 ,12 ], [3 ,11 ],[2 ,10 ],[0 ,10 ],[2 ,10 ],[3 ,11 ],[2 ,10 ],[3 ,11 ],[2 ,10 ],[3 ,11 ],[2 ,10 ],[0 ,10 ],[2 ,10 ],[3 ,11 ],[2 ,10 ],[3 ,11 ],[2 ,10 ],[2 ,9 ] ])
