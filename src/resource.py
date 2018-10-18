


'''the position of widgets in sam page'''
VAL = {}
VAL['X0'] = 0.115
VAL['X1'] = 0.862
VAL['Y'] = 0.324


ACT = {}
ACT['X0'] = 0.115
ACT['X1'] = 0.862
ACT['Y'] = 0.604

CTR = {}
CTR['X0'] = 0.115
CTR['X1'] = 0.862
CTR['Y'] = 0.897

'''the position of widgets in emotion page'''

EMOTIONS_CENTER = [0.50, 0.539]
EMOTIONS = {}
EMOTIONS['Happy'] = (0.813, 0.482)
EMOTIONS['Delighted'] = (0.801, 0.423)
EMOTIONS['Amused'] = (0.776,0.368)
EMOTIONS['Excited'] = (0.740, 0.312)
EMOTIONS['Astonished'] = (0.682, 0.254)
EMOTIONS['Aroused'] = (0.561, 0.198)

EMOTIONS['Embarassed']  = (2*EMOTIONS_CENTER[0] - EMOTIONS['Happy'][0],         EMOTIONS['Happy'][1])     
EMOTIONS['Frustrated']  = (2*EMOTIONS_CENTER[0] - EMOTIONS['Delighted'][0],      EMOTIONS['Delighted'][1] )
EMOTIONS['Annoyed']     = (2*EMOTIONS_CENTER[0] - EMOTIONS['Amused'][0],          EMOTIONS['Amused'][1]    )
EMOTIONS['Anger']       = (2*EMOTIONS_CENTER[0] - EMOTIONS['Excited'][0],       EMOTIONS['Excited'][1]   )
EMOTIONS['Afraid']      = (2*EMOTIONS_CENTER[0] - EMOTIONS['Astonished'][0], EMOTIONS['Astonished'][1])
EMOTIONS['Alarmed']     = (2*EMOTIONS_CENTER[0] - EMOTIONS['Aroused'][0],    EMOTIONS['Aroused'][1]   )

EMOTIONS['Miserable']   = (2*EMOTIONS_CENTER[0] - EMOTIONS['Happy'][0]      , 2*EMOTIONS_CENTER[1] - EMOTIONS['Happy'][1])
EMOTIONS['Sad']         = (2*EMOTIONS_CENTER[0] - EMOTIONS['Delighted'][0]  , 2*EMOTIONS_CENTER[1] - EMOTIONS['Delighted'][1])
EMOTIONS['Gloomy']      = (2*EMOTIONS_CENTER[0] - EMOTIONS['Amused'][0] ,2*EMOTIONS_CENTER[1] - EMOTIONS['Amused'][1])
EMOTIONS['Depressed']   = (2*EMOTIONS_CENTER[0] - EMOTIONS['Excited'][0]   , 2*EMOTIONS_CENTER[1] - EMOTIONS['Excited'][1])
EMOTIONS['Bored']       = (2*EMOTIONS_CENTER[0] - EMOTIONS['Astonished'][0]   , 2*EMOTIONS_CENTER[1] - EMOTIONS['Astonished'][1])
EMOTIONS['Tired']       = (2*EMOTIONS_CENTER[0] - EMOTIONS['Aroused'][0], 2*EMOTIONS_CENTER[1] - EMOTIONS['Aroused'][1])

EMOTIONS['Glad'] =      (EMOTIONS['Happy'][0],          2*EMOTIONS_CENTER[1] - EMOTIONS['Happy'][1])  
EMOTIONS['Pleased'] =   (EMOTIONS['Delighted'][0],      2*EMOTIONS_CENTER[1] - EMOTIONS['Delighted'][1])  
EMOTIONS['Satisfied'] = (EMOTIONS['Amused'][0],         2*EMOTIONS_CENTER[1] - EMOTIONS['Amused'][1])  
EMOTIONS['Serene'] =    (EMOTIONS['Excited'][0],        2*EMOTIONS_CENTER[1] - EMOTIONS['Excited'][1])  
EMOTIONS['Relaxed'] =   (EMOTIONS['Astonished'][0],     2*EMOTIONS_CENTER[1] - EMOTIONS['Astonished'][1])  
EMOTIONS['Calm'] =      (EMOTIONS['Aroused'][0],        2*EMOTIONS_CENTER[1] - EMOTIONS['Aroused'][1])  

