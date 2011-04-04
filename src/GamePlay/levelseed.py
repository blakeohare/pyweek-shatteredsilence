class LevelSeed:
    def __init__(self, special=None, args=None):
        self.width = 64
        self.height = 64
        self.mode = 'individual'
        if special != None:
            self.InitializeSpecialLevel(special)
        else:
            self.width = args['width']
            self.height = args['height']
            self.mode = args['mode']
            self.progress = args['progress']
            self.timedMode = args['minutes'] > -1
            self.minutes = args['minutes']
            
            if self.mode == 'individual':
                self.citizens = args['citizens']
                self.police = args['police']
            else:
                self.citizens = 0
                self.police = 0
            
            if self.mode == 'region':
                self.city_centers = args['city_centers']
            else:
                self.city_centers = 0
                    
    def InitializeSpecialLevel(self, special):
        self.progress = True
        self.timedMode = False
        self.police = 0
        if special == 'testlevel':
            self.progress = False
            self.width = 32
            self.height = 24
            self.citizens = 10
            self.police = 2
        elif special == 'level1':
            self.width = 20
            self.height = 15
            self.citizens = 1
        elif special == 'level2':
            self.width = 32
            self.height = 24
            self.citizens = 9
        elif special == 'level3':
            self.width = 64
            self.height = 48
            self.citizens = 30
            self.police = 3
        elif special == 'level4':
            self.width = 180
            self.height = 100
            self.citizens = 100
            self.police = 20
        elif special == 'level5':
            self.mode = 'crowd'
            self.width = 40
            self.height = 32
        elif special == 'level6':
            self.mode = 'crowd'
            self.width = 96
            self.height = 64
        elif special == 'level7':
            self.mode = 'crowd'
            self.width = 180
            self.height = 100
        elif special == 'level8':
            self.mode = 'region'
            self.width = 40
            self.height = 32
        elif special == 'level9':
            self.mode = 'region'
            self.width = 96
            self.height = 64
    