# %% Import libraries
import numpy as np
import random
import os
import re
import librosa
import soundfile as sf
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def random_elem_in_list(list_of_elems):
    return list_of_elems[random.randint(0,len(list_of_elems)-1)]
# %% YOUR CODE HERE

# ==== GRAMMARS
basic_grammar={
    "S":["M", "SM"],
    "M": ["HH"],    
    "H": ["h", "qq"],
}

slow_grammar={
    "S":["M", "SM"],
    "M": ["HH","w", "$w"],    
    "H": ["h", "$h"],
}

octave_grammar={
    "S":["M", "SM"],
    "M": ["HH"],    
    "H": ["h", "QQ"],
    "Q": ["q", "oo"],
}

triplet_grammar={
    "S":["M", "SM"],
    "M": ["HH", "ththth"],    
    "H": ["h", "QQ","tqtqtq","$h"],
    "Q": ["q", "OO", "oo", "tototo","$q"],
    "O": ["o", "$o"]
}
upbeat_grammar={
    "S":["M", "SM"],
    "M": ["HH", "ththth","VVV", "QHQ"],    
    "H": ["h", "QQ","tqtqtq","$h", "otototoo", "OQO"],
    "V": ["th", "ph"], 
    "Q": ["q", "OO", "oo", "tototo","$q", "potopo", "popoto"],
    "O": ["o", "$o"]
}

# === Words to duration ===
word_dur={"h":0.5, # half-measure
          "q":0.25, # quarter-measure
          "o":1/8, # quarter-measure
          "$h": 0.5,
          "$q": 0.25,
          "$o": 1/8,
          "th": 1/3,
          "tq": 1/6,
          "to": 1/12,
          "ph": 1/3,
          "pq": 1/6,
          "po": 1/12,
          "w": 1,
          "$w": 1,          
}

# write_mix
def write_mix(Cs, gains=None, fn_out="out.wav"):
    # your code
    tracks = []
    len_sequence = []
    for i in range(len(Cs)):
        tracks.append(Cs[i].sequence)
        len_sequence.append(len(tracks[i]))
    track = np.zeros(np.min(len_sequence))
    for i in range(len(samples)):
        track = track + tracks[i][0:len(track)]*gains[i]                           
    track=0.707*track/np.max(np.abs(track))
    sf.write(fn_out, track, Cs[0].sr)

# %% Grammar Sequence
class Grammar_Sequence:
    def __init__(self, grammar):
        self.grammar=grammar
        self.grammar_keys=list(grammar.keys())
        self.N=len(self.grammar_keys)
        self.sequence=""
       
    def find_symbol(self, symbol):
        return [m.start() for m in re.finditer(symbol, self.sequence)]
    def replace(self, index, symbol, convert_to):
        len_symbol=len(symbol)
        self.sequence=self.sequence[:index]+convert_to+self.sequence[index+len_symbol:]
    def convert_sequence(self):        
        symbol=random_elem_in_list(self.grammar_keys)
        while symbol not in self.sequence:
            symbol=random_elem_in_list(self.grammar_keys)
            
        index=random_elem_in_list(self.find_symbol(symbol))
        convert_to= random_elem_in_list(self.grammar[symbol])
        self.replace(index, symbol, convert_to)
        
    def create_sequence(self, start_sequence):
        self.sequence=start_sequence
        sequence_transformation=[start_sequence]
        while (self.sequence!=self.sequence.lower()):
            self.convert_sequence()
            sequence_transformation.append(self.sequence)
        return sequence_transformation
# %% Composer
class Composer():
    def __init__(self, fn, sr=-1, BPM=120):
        if sr==-1:
            self.sample, self.sr =  librosa.load(fn)     
        else:
            self.sample, self.sr =  librosa.load(fn,sr=sr)         
        self.sampleN=self.sample.size
        self.BPM= BPM
        self.q_bpm=60/self.BPM
        self.m_bpm=4*self.q_bpm
        self.sequence=[]
    def split_sequence(self, sequence):
        k=0
        sym_seq=[]
        dur_seq=[]
        while k<len(sequence):
            if sequence[k] in "$tp":
                #your code 
                sym=sequence[k]+sequence[k+1]
                k+=2        
            else:
                sym=sequence[k]
                k+=1
            sym_seq.append(sym)
            
            dur_seq.append(word_dur[sym])
        return dur_seq, sym_seq
    def compute_duration(self, dur_seq):
        duration_in_notes=0
        for dur in dur_seq:
            duration_in_notes+=dur
        return duration_in_notes        
    def create_sequence(self, sequence):
        dur_seq, sym_seq=self.split_sequence(sequence)
        duration_in_notes=self.compute_duration(dur_seq)
        
        duration_in_seconds=duration_in_notes*self.m_bpm
        self.sequence=np.zeros((int(duration_in_seconds*self.sr),))
        idx=0
        for note, symbol in zip(dur_seq, sym_seq):
            if not symbol.startswith("$"):
                if self.sequence.size > idx+self.sampleN: 
                    self.sequence[idx:idx+self.sampleN]+=self.sample
                else:
                    K=self.sequence.size-idx
                    self.sequence[idx:]+=self.sample[:K]
                    self.sequence[:self.sampleN-K]+=self.sample[K:]
            idx+=int(note*self.sr*self.m_bpm)
    def write(self, fn_out="out.wav", repeat=1, write=True):
        sequence_to_write=np.repeat(self.sequence, (repeat,))
        if write:
            sf.write(fn_out, sequence_to_write, self.sr)
        else:
            return sequence_to_write

# %% main script
if __name__=="__main__":
    EX=7
    C=None
    NUM_M=8
    START_SEQUENCE="M"*NUM_M
    MONO_COMPOSITION=EX<7
    if EX==1:
        G=Grammar_Sequence(basic_grammar)        
        fn_out="basic_composition.wav"
    elif EX==2:
        G=Grammar_Sequence(octave_grammar)
        fn_out="octave_composition.wav"
    elif EX==3:
        G=Grammar_Sequence(triplet_grammar)
        fn_out="triplet_composition.wav"
    elif EX==4:
        G=Grammar_Sequence(slow_grammar)
        fn_out="slow_composition.wav"
    elif EX==5:        
        G=Grammar_Sequence(upbeat_grammar)        
        fn_out="upbeat_composition.wav"
    elif EX==6:
        G=Grammar_Sequence(clave_grammar)
        fn_out="clave_composition.wav"
    elif EX==7:
        samples=[
            "sounds/fkick_02a.wav",
            "sounds/D4cymb19.wav",
            "sounds/Rimsd1.wav",
            "sounds/Rimsd1.wav",
            "sounds/snar_07a.wav",
            "sounds/tr_hrk_bd_02_a.wav",
            "sounds/tr_hrk_scratch_02_a.wav"
        ]
        grammars=[
            upbeat_grammar,
            basic_grammar,
            triplet_grammar,
            slow_grammar,
            basic_grammar,
            slow_grammar,
            octave_grammar
        ]# your grammars
        gains = [
            1,
            0.7,
            0.8,
            0,
            0.5,
            0,
            0.7
        ] #your gains
        fn_out="multitrack.wav"
        Gs=[]  #list of Grammar_Sequence
        Cs=[]  #list of Composer
        SR=16000 # use a common sr
        for i in range(len(samples)):
            Gs.append(Grammar_Sequence(grammars[i])) 
            Cs.append(Composer(samples[i], SR, BPM=120))
            Gs[i].create_sequence(START_SEQUENCE)
            Cs[i].create_sequence(Gs[i].sequence)
    if MONO_COMPOSITION:
        seqs=G.create_sequence(START_SEQUENCE)
        print("\n".join(seqs), "\nFinal sequence: ", G.sequence)    
        #C= Composer("sounds/fkick_02a.wav", BPM=174)

        C= Composer("sounds/D4cymb19.wav", BPM=150)
        C.create_sequence(G.sequence)
        C.write("out/"+fn_out)
    else:
        write_mix(Cs, gains=gains, fn_out="out/multitrack.wav")