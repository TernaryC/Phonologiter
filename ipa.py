import tkinter as tk

IPA_Place = ["Bilabial", "Labiodental", "Dental", "Alveolar", "Postalveolar", 
             "Retroflex", "Palatal", "Velar", "Uvular", "Pharyngeal", "Glottal"]
IPA_Manner = ["Plosive", "Nasal", "Trill", "Tap or Flap", "Fricative",        
              "Other Fricative", "Approximant", "Other Approximant"]

IPA_Backness = ["Front", "Near-Front", "Central", "Near-Back", "Back"]
IPA_Height = ["Close", "Close-Mid", "Mid", "Open-Mid", "Open"]

IPA_Type = ["Clicks", "Implosives", "Ejectives"]
IPA_i = [0, 1, 2, 3, 4]

IPA_TOP = [
           [
            "bilab", "labio", "denta", "alveo", "posta", "retro", "palat",
            "velar", "uvula", "phary", "glott"
           ],
           [
            "front", "nfron", "centr", "nback", "back"
           ],
           [
            "click", "implo", "eject"
           ]
          ]
IPA_SIDE = [
            [
             "plosi", "nasal", "trill", "tap", "frica", "ofric", "appro",
             "oappr"
            ],
            [
             "close", "clmid", "mid", "opmid", "open"
            ],
            [
             "0", "1", "2", "3", "4"
            ]
           ]


BILAB = IPA_Place[0]; LABIO = IPA_Place[1]; DENTA = IPA_Place[2]
ALVEO = IPA_Place[3]; POSTA = IPA_Place[4]; RETRO = IPA_Place[5]
PALAT = IPA_Place[6]; VELAR = IPA_Place[7]; UVULA = IPA_Place[8]
PHARY = IPA_Place[9]; GLOTT = IPA_Place[10]

PLOSI = IPA_Manner[0]; NASAL = IPA_Manner[1]; TRILL = IPA_Manner[2]
TAPOR = IPA_Manner[3]; FRICA = IPA_Manner[4]; LATFR = IPA_Manner[5]
APPRO = IPA_Manner[6]; LATAP = IPA_Manner[7]


FRONT = IPA_Backness[0]; NEARF = IPA_Backness[1]; CENTR = IPA_Backness[2]
NEARB = IPA_Backness[3]; BACKK = IPA_Backness[4]

CLOSE = IPA_Height[0]; CLMID = IPA_Height[1]; TRMID = IPA_Height[2]
OPMID = IPA_Height[3]; OPENN = IPA_Height[4]


CLICK = IPA_Type[0]; IMPLO = IPA_Type[1]; EJECT = IPA_Type[2]



def sort_IPA(set, type, side):
    if type == 0: ipa = IPA_Manner if side else IPA_Place
    if type == 1: ipa = IPA_Height if side else IPA_Backness
    if type == 2: ipa = IPA_i if side else IPA_Type
    
    nset = ["" for _ in ipa]
    for v in set:
        nset[ipa.index(v)] = v
    return [i for i in nset if i != ""]




class IPA_Symb:
    def __init__(self, symb, col, row, voice, type):
        self.symb = symb
        
        self.c = col
        self.r = row
        self.voice = voice
        
        self.type = type
        
        self.active = False
        
    def id(self):
        j = self.row()
        if self.type == 0: i = IPA_Place.index(self.c)
        if self.type == 1: i = IPA_Backness.index(self.c)
        if self.type == 2: i = IPA_Type.index(self.c)
        id = str(self.type) + "/" + IPA_TOP[self.type][i]
        id += "_" + IPA_SIDE[self.type][j]
        id += "_1" if self.voice else "_0"
        return id
        
    def col(self, set=None):
        if set != None: return set.index(self.c) * 2 + (1 if self.voice else 0)
        if self.type == 0:
            return IPA_Place.index(self.c) * 2 + (1 if self.voice else 0)
        elif self.type == 1:
            return IPA_Backness.index(self.c) * 2 + (1 if self.voice else 0)
        elif self.type == 2 or self.type == 3:
            return IPA_Type.index(self.c) * 2 + (1 if self.voice else 0)
        
    def row(self, set=None):
        if set != None: return set.index(self.r)
        if self.type == 0:
            return IPA_Manner.index(self.r)
        elif self.type == 1:
            return IPA_Height.index(self.r)
        elif self.type == 2 or self.type == 3:
            return IPA_i.index(self.r)
        
    def anc(self):
        return tk.W if self.voice else tk.E

IPA = {
      # &             &   Place  Manner Voice
      # Plosives
       'p': IPA_Symb('p', BILAB, PLOSI, False, 0),
       'b': IPA_Symb('b', BILAB, PLOSI,  True, 0),
       't': IPA_Symb('t', ALVEO, PLOSI, False, 0),
       'd': IPA_Symb('d', ALVEO, PLOSI,  True, 0),
       'ʈ': IPA_Symb('ʈ', RETRO, PLOSI, False, 0),
       'ɖ': IPA_Symb('ɖ', RETRO, PLOSI,  True, 0),
       'c': IPA_Symb('c', PALAT, PLOSI, False, 0),
       'ɟ': IPA_Symb('ɟ', PALAT, PLOSI,  True, 0),
       'k': IPA_Symb('k', VELAR, PLOSI, False, 0),
       'ɡ': IPA_Symb('ɡ', VELAR, PLOSI,  True, 0),
       'q': IPA_Symb('q', UVULA, PLOSI, False, 0),
       'ɢ': IPA_Symb('ɢ', UVULA, PLOSI,  True, 0),
       'ʔ': IPA_Symb('ʔ', GLOTT, PLOSI, False, 0),
      # Nasal
       'm': IPA_Symb('m', BILAB, NASAL,  True, 0),
       'ɱ': IPA_Symb('ɱ', LABIO, NASAL,  True, 0),
       'n': IPA_Symb('n', ALVEO, NASAL,  True, 0),
       'ɳ': IPA_Symb('ɳ', RETRO, NASAL,  True, 0),
       'ɲ': IPA_Symb('ɲ', PALAT, NASAL,  True, 0),
       'ŋ': IPA_Symb('ŋ', VELAR, NASAL,  True, 0),
       'ɴ': IPA_Symb('ɴ', UVULA, NASAL,  True, 0),
      # Trill
       'ʙ': IPA_Symb('ʙ', BILAB, TRILL,  True, 0),
       'r': IPA_Symb('r', ALVEO, TRILL,  True, 0),
       'ʀ': IPA_Symb('ʀ', UVULA, TRILL,  True, 0),
      # Tap or Flap
       'ⱱ': IPA_Symb('ⱱ', LABIO, TAPOR,  True, 0),
       'ɾ': IPA_Symb('ɾ', ALVEO, TAPOR,  True, 0),
       'ɽ': IPA_Symb('ɽ', RETRO, TAPOR,  True, 0),
      # Fricative
       'ɸ': IPA_Symb('ɸ', BILAB, FRICA, False, 0),
       'β': IPA_Symb('β', BILAB, FRICA,  True, 0),
       'f': IPA_Symb('f', LABIO, FRICA, False, 0),
       'v': IPA_Symb('v', LABIO, FRICA,  True, 0),
       'θ': IPA_Symb('θ', DENTA, FRICA, False, 0),
       'ð': IPA_Symb('ð', DENTA, FRICA,  True, 0),
       's': IPA_Symb('s', ALVEO, FRICA, False, 0),
       'z': IPA_Symb('z', ALVEO, FRICA,  True, 0),
       'ʃ': IPA_Symb('ʃ', POSTA, FRICA, False, 0),
       'ʒ': IPA_Symb('ʒ', POSTA, FRICA,  True, 0),
       'ʂ': IPA_Symb('ʂ', RETRO, FRICA, False, 0),
       'ʐ': IPA_Symb('ʐ', RETRO, FRICA,  True, 0),
       'ç': IPA_Symb('ç', PALAT, FRICA, False, 0),
       'ʝ': IPA_Symb('ʝ', PALAT, FRICA,  True, 0),
       'x': IPA_Symb('x', VELAR, FRICA, False, 0),
       'ɣ': IPA_Symb('ɣ', VELAR, FRICA,  True, 0),
       'χ': IPA_Symb('χ', UVULA, FRICA, False, 0),
       'ʁ': IPA_Symb('ʁ', UVULA, FRICA,  True, 0),
       'ħ': IPA_Symb('ħ', PHARY, FRICA, False, 0),
       'ʕ': IPA_Symb('ʕ', PHARY, FRICA,  True, 0),
       'h': IPA_Symb('h', GLOTT, FRICA, False, 0),
       'ɦ': IPA_Symb('ɦ', GLOTT, FRICA,  True, 0),
      # Lateral Fricative
       'ɬ': IPA_Symb('ɬ', ALVEO, LATFR, False, 0),
       'ɮ': IPA_Symb('ɮ', ALVEO, LATFR,  True, 0),
      # Approximate
       'ʋ': IPA_Symb('ʋ', LABIO, APPRO,  True, 0),
       'ɹ': IPA_Symb('ɹ', ALVEO, APPRO,  True, 0),
       'ɻ': IPA_Symb('ɻ', RETRO, APPRO,  True, 0),
       'j': IPA_Symb('j', PALAT, APPRO,  True, 0),
       'ɰ': IPA_Symb('ɰ', VELAR, APPRO,  True, 0),
      # Lateral Approximate
       'l': IPA_Symb('l', ALVEO, LATAP,  True, 0),
       'ɭ': IPA_Symb('ɭ', RETRO, LATAP,  True, 0),
       'ʎ': IPA_Symb('ʎ', PALAT, LATAP,  True, 0),
       'ʟ': IPA_Symb('ʟ', VELAR, LATAP,  True, 0),
       
      # &             &   Back   Height Round
      # Close
       'i': IPA_Symb('i', FRONT, CLOSE, False, 1),
       'y': IPA_Symb('y', FRONT, CLOSE,  True, 1),
       'ɨ': IPA_Symb('ɨ', CENTR, CLOSE, False, 1),
       'ʉ': IPA_Symb('ʉ', CENTR, CLOSE,  True, 1),
       'ɯ': IPA_Symb('ɯ', BACKK, CLOSE, False, 1),
       'u': IPA_Symb('u', BACKK, CLOSE,  True, 1),
       'ɪ': IPA_Symb('ɪ', NEARF, CLOSE, False, 1),
       'ʏ': IPA_Symb('ʏ', NEARF, CLOSE,  True, 1),
       'ʊ': IPA_Symb('ʊ', NEARB, CLOSE,  True, 1),
      # Close-Mid
       'e': IPA_Symb('e', FRONT, CLMID, False, 1),
       'ø': IPA_Symb('ø', FRONT, CLMID,  True, 1),
       'ɘ': IPA_Symb('ɘ', CENTR, CLMID, False, 1),
       'ɵ': IPA_Symb('ɵ', CENTR, CLMID,  True, 1),
       'ɤ': IPA_Symb('ɤ', BACKK, CLMID, False, 1),
       'o': IPA_Symb('o', BACKK, CLMID,  True, 1),
      # Mid
       'ə': IPA_Symb('ə', CENTR, TRMID,  True, 1),
      # Open-Mid
       'ɛ': IPA_Symb('ɛ', FRONT, OPMID, False, 1),
       'œ': IPA_Symb('œ', FRONT, OPMID,  True, 1),
       'æ': IPA_Symb('æ', NEARF, OPMID,  True, 1),
       'ɜ': IPA_Symb('ɜ', CENTR, OPMID, False, 1),
       'ɞ': IPA_Symb('ɞ', CENTR, OPMID,  True, 1),
       'ɐ': IPA_Symb('ɐ', NEARB, OPMID,  True, 1),
       'ʌ': IPA_Symb('ʌ', BACKK, OPMID, False, 1),
       'ɔ': IPA_Symb('ɔ', BACKK, OPMID,  True, 1),
      # Open
       'a': IPA_Symb('a', CENTR, OPENN, False, 1),
       'ɶ': IPA_Symb('ɶ', CENTR, OPENN,  True, 1),
       'ä': IPA_Symb('ä', NEARB, OPENN,  True, 1),
       'ɑ': IPA_Symb('ɑ', BACKK, OPENN, False, 1),
       'ɒ': IPA_Symb('ɒ', BACKK, OPENN,  True, 1),
       
      # &             &   Type   i 
      # Clicks
       'ʘ': IPA_Symb('ʘ', CLICK, 0,      True, 2),
       'ǀ': IPA_Symb('ǀ', CLICK, 1,      True, 2),
       'ǃ': IPA_Symb('ǃ', CLICK, 2,      True, 2),
       'ǂ': IPA_Symb('ǂ', CLICK, 3,      True, 2),
       'ǁ': IPA_Symb('ǁ', CLICK, 4,      True, 2),
      # Implosives
       'ɓ': IPA_Symb('ɓ', IMPLO, 0,      True, 2),
       'ɗ': IPA_Symb('ɗ', IMPLO, 1,      True, 2),
       'ʄ': IPA_Symb('ʄ', IMPLO, 2,      True, 2),
       'ɠ': IPA_Symb('ɠ', IMPLO, 3,      True, 2),
       'ʛ': IPA_Symb('ʛ', IMPLO, 4,      True, 2),
      # Ejectives
       'p\'': IPA_Symb('p\'', EJECT, 0,  True, 2),
       't\'': IPA_Symb('t\'', EJECT, 1,  True, 2),
       'k\'': IPA_Symb('k\'', EJECT, 2,  True, 2),
       's\'': IPA_Symb('s\'', EJECT, 3,  True, 2),
      # Other
       'ʍ':   IPA_Symb('ʍ',   BILAB, LATFR, False, 0),
       'w':   IPA_Symb('w',   BILAB, APPRO,  True, 0),
       'ʜ':   IPA_Symb('ʜ',   GLOTT, TRILL, False, 0),
       'ɥ':   IPA_Symb('ɥ',   BILAB, LATAP,  True, 0),
       'ʢ':   IPA_Symb('ʢ',   GLOTT, TRILL,  True, 0),
       '(ʡ)': IPA_Symb('(ʡ)', GLOTT, PLOSI,  True, 0),
       'ɕ':   IPA_Symb('ɕ',   PALAT, LATFR, False, 0),
       'ʑ':   IPA_Symb('ʑ',   PALAT, LATFR,  True, 0),
       '(ɺ)': IPA_Symb('(ɺ)', ALVEO, TAPOR, False, 0),
       'ɧ':   IPA_Symb('ɧ',   VELAR, LATFR, False, 0),
      }
      
IPA_Other = {
       
      }