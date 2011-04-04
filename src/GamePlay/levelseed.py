class LevelSeed:
    def __init__(self, special=None, args=None):
        self.width = 64
        self.height = 64
        self.mode = 'individual'
        if special != None:
            self.InitializeSpecialLevel(special)
        
        # TODO: initialize custom level
            
    def InitializeSpecialLevel(self, special):
        if special == 'testlevel':
            self.width = 32
            self.height = 24
        elif special == 'level1':
            self.width = 32
            self.height = 24
        elif special == 'level2':
            self.width = 40
            self.height = 32
        elif special == 'level3':
            self.width = 96
            self.height = 64
        elif special == 'level4':
            self.width = 180
            self.height = 100
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
    