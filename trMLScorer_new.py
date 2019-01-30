from LoadInvertedIndex import load_inverted_idx
from LoadPrTr import load_tr_pr
from LoadBackgroud import load_background

invert = load_inverted_idx('')
translation_pr = load_tr_pr('tr_pr.txt')        
background = load_background('source.vcb')

class trML_scorer():

    def __init__(self,queryid:str,query_tokenized:str,candidateid,lamb,alpha,beta,gamma,topn=30):
        self.queryid = queryid
        self.candidateid = candidateid
        self.query_tokenized = query_tokenized.strip().split()
        self.lamb,self.alpha,self.beta,self.gamma = lamb,alpha,beta,gamma
        self.topn = topn

    def retrieval(self):
        from collections import defaultdict
        import heapq
        all_result = defaultdict(float)
        for query_w in self.query_tokenized:
            result = defaultdict(float)
            for word,pr in list(filter(lambda x: x[1] > 0.01, translation_pr[query_w])):
                try:
                    df, start_idx = invert.lexicon_question[word]
                    relevant_dict = {qid:count for qid,count in invert.posting_question[start_idx:start_idx+df]}
                    for qid in set(self.candidateid).intersection(relevant_dict.keys()):
                        count_word_q = relevant_dict[qid]
                        len_q = invert.QAlength[qid][0]
                        result[qid] += self.beta*pr*count_word_q/len_q
                except KeyError:
                    pass
            try:
                df, start_idx = invert.lexicon_question[query_w]
                relevant_dict = {qid:count for qid,count in invert.posting_question[start_idx:start_idx+df]}
                for qid in set(self.candidateid).intersection(relevant_dict.keys()):
                    count_word_q = relevant_dict[qid]
                    len_q = invert.QAlength[qid][0]
                    result[qid] += self.alpha*count_word_q/len_q
            except KeyError:
                pass
            
            try:
                df, start_idx = invert.lexicon_ans[query_w]
                relevant_dict = {qid:count for qid,count in invert.posting_ans[start_idx:start_idx+df]}
                for qid in set(self.candidateid).intersection(relevant_dict.keys()):
                    count_word_ans = relevant_dict[qid]
                    len_ans = invert.QAlength[qid][1]
                    result[qid] += self.gamma*count_word_ans/len_ans
            except KeyError:
                pass

            for qid in self.candidateid:
                import numpy as np
                len_total = sum(invert.QAlength[qid])
                result[qid] = np.log(len_total/(len_total+self.lamb)*result[qid]+self.lamb/(len_total+self.lamb)*background[query_w])
                all_result[qid] += result[qid]
        
        return([self.queryid]+heapq.nlargest(self.topn, all_result, key=all_result.get))

if __name__ == '__main__':
    testset = {}
    with open(r'testset.txt','r') as f:
        for i,line in enumerate(f):
            qid, question = line.strip().split('\t')
            testset[qid] = question
    
    candidateid_dict = {}
    with open(r'testid&candidateid.txt','r') as f:
        for line in f:
            qid, candidateid = line.strip().split('\t')
            candidateid_dict[qid] = candidateid.strip().split()

    for alpha,beta,gamma in [[0.6,0.1,0.3],[0.3,0.1,0.6]]:
        testresult = []
        i = 0
        for qid in testset.keys():
            mytrML = trML_scorer(qid,testset[qid],candidateid_dict[qid],20,alpha,beta,gamma)
            testresult.append(mytrML.retrieval())
            i += 1
            print(i)
        
        filename = '-'.join(['new',str(alpha),str(beta),str(gamma),'testresult.txt'])
        with open(filename,'w') as f:
            for value in testresult:
                print(value[0],file = f)
                print(' '.join(value[1:]),file = f)


