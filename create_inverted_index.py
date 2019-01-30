class inverted_idx():
    """
    posting file is a list of tuple
    lexicon is a dictionary with words being keys
    """
    def __init__(self,input_path):
        self.input_path = input_path
        self.QAlength = {}
        self.posting_question = None
        self.posting_ans = None
        self.lexicon_question = None
        self.lexicon_ans = None
        self.build_inverted_index()

    def parse_count(self,qid:str,mystring:str,result:list):
        from collections import Counter
        mydict = Counter(mystring.split())
        for word,count in zip(mydict.keys(),mydict.values()):
            result.append((word,qid,count))

    def create_posting(self,data:list):
        from operator import itemgetter
        return sorted(data,key=itemgetter(0))

    def posting2lexicon(self,myposting:list):
        d = {}
        for i,value in enumerate(myposting):
            if value[0] in d:
                d[value[0]][0] += 1
            else:
                d[value[0]] = [1]
                d[value[0]].append(i)
        return d
    
    def build_inverted_index(self):
        with open(self.input_path,'r') as f:
            Parse_question = []
            Parse_ans = []
            for i,line in enumerate(f):
                id, question, ans1, ans2 = line.split('\t')
                ans2 = ans2.strip()
                self.QAlength[id] = (len(question),len(ans1+ans2))
                self.parse_count(id,question,Parse_question)
                self.parse_count(id,ans1+ans2,Parse_ans)
            self.posting_question = self.create_posting(Parse_question)
            self.posting_ans = self.create_posting(Parse_ans)
            self.lexicon_question = self.posting2lexicon(self.posting_question)
            self.lexicon_ans = self.posting2lexicon(self.posting_ans)

    def posting2txt(self,path:str,content:list):
        with open(path,'w') as f:
            print('wordid qid freq',file = f)
            for i in content:
                print(i[0],i[1],i[2],file = f)

    def lexicon2txt(self,path:str,content:dict):
        with open(path,'w') as f:
            print('wordid df start_index',file = f)
            for key,value in zip(content.keys(),content.values()):
                print(key,value[0],value[1],file = f)

invert = inverted_idx(r'/python_qid2all_tokenized.txt')

invert.posting2txt(r'/posting_question.txt',invert.posting_question)
invert.posting2txt(r'/posting_ans.txt',invert.posting_ans)

invert.lexicon2txt(r'/lexicon_question.txt',invert.lexicon_question)
invert.lexicon2txt(r'/lexicon_ans.txt',invert.lexicon_ans)

with open(r'/home/ryanhuang121/python_QAlength.txt','w') as f:
    print('qid q_len ans_len',file = f)
    for key,value in zip(invert.QAlength.keys(),invert.QAlength.values()):
        print(key,value[0],value[1],file = f)
