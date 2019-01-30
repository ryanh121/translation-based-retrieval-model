def load_tr_pr(path):
    """
    return a dictionary with keys being target_id:str
    """
    from collections import defaultdict
    pr_tr = defaultdict(list)
    with open(path,'r') as f:
        for line in f:
            target_id, source_id, pr = line.strip().split()
            pr_tr[target_id] += [(source_id,float(pr))]
    print('load_pr_tr laoded!')
    return pr_tr
