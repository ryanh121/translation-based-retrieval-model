class load_inverted_idx():

    def __init__(self,input_path):
        self.input_path = input_path
        self.QAlength = {}
        self.posting_question = []
        self.posting_ans = []
        self.lexicon_question = {}
        self.lexicon_ans = {}
        self.load_QAlength('python_QAlength.txt',self.QAlength)
        self.load_posting('posting_question.txt',self.posting_question)
        self.load_posting('posting_ans.txt',self.posting_ans)
        self.load_lexicon('lexicon_question.txt',self.lexicon_question)
        self.load_lexicon('lexicon_ans.txt',self.lexicon_ans)


    def load_posting(self,filename:str,result):
        with open(self.input_path+filename,'r') as f:
            next(f)
            for line in f:
                wordid, qid, freq = line.strip().split()
                result.append([qid,int(freq)])
        print(' '.join([filename,'loaded!']))
    
    def load_lexicon(self,filename:str,result):
        with open(self.input_path+filename,'r') as f:
            next(f)
            for line in f:
                wordid, df, start_index = line.strip().split()
                result[wordid] = (int(df),int(start_index))
        print(' '.join([filename,'loaded!']))
    
    def load_QAlength(self,filename,result):
        with open(self.input_path+filename,'r') as f:
            next(f)
            for line in f:
                qid, q_len, ans_len = line.strip().split()
                result[qid] = (int(q_len),int(ans_len))
        print(' '.join([filename,'loaded!']))
