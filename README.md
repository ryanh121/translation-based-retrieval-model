# Translation-Based Retrieval Model with Inverted Index
## Dataset
The [LinkSO dataset](https://sites.google.com/view/linkso) contains Stack Overflow questions in three programming languages: Java, JavaScript and Python. Each folder contains the following files:
1. The questions and answers: language_qid2all.txt
2. The linked (and unlinked questions): language_cosidf.txt
3. The training/development/testing folds: language_train/dev/test_qid.txt
## Implementation
1. Learn word-to-word translation probabilities with [GIZA++](http://www.statmt.org/moses/giza/GIZA++.html) toolkit
2. Build inverted index data structures for questions and answers
3. Compute background probabilities
4. Combine inverted index data structures with the translation-based retrieval model (Pseudocode is shown as follows)
```
for every query term q in Q
	// look up translation table, T: term list, P: probability list
	< T, P > = lookup(q,threshold)
	// add term q into the term list and the probability list
	< T, P > = < T, P > + (q, 1.0)
	for each term t in T
		// get document list D from inverted index of question part, 
		// and find intersection with candidate q2
		D = candidateq2.intersection(question_getDocList(t))
		for every document d in D
			// Maximum likelihood estimation
			P_ml = frequency(t,d) / docLength(d)
			// translation-based estimation
			if t == q // matching term
				termScoreBuf[d] += alpha*P_ml
			else // expanded terms
				termScoreBuf[d] += beta*P_ml*P(q|t)
		end
	end
	// get document list D from inverted index of answer part,
	// and find intersection with candidate q2
	D = candidateq2.intersection(answer_getDocList(t))
	for every document d in D
		// Maximum likelihood estimation
		termScoreBuf[d] += = gamma*frequency(q,d) / docLength(d)
	for every document d in the candidateq2
		// background smoothing
		termScoreBuf[d] = len(d)/(len(d)+lambda)*termScoreBuf[d] + lambda/(len(d)+lambda)*collectionLM[q]
		// add term score into the final results
		results[d] += log(termScoreBuf[d])
	end
end
```
## References
1. [LinkSO: A Dataset for Learning to Retrieve Similar Question Answer Pairs on Software Development Forums](http://xliu93.web.illinois.edu/pdf/nl4se18.pdf)
2. [Retrieval Models for Question and Answer Archives](http://maroo.cs.umass.edu/getpdf.php?id=811)
