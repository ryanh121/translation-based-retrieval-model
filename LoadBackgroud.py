def load_background(path):
    """
    return a dictionary of background probabilities
    """
    total_count = 0
    with open(path,'r') as f:
        background_pr = {}
        for line in f:
            id, word, count = line.strip().split()
            count = int(count)
            background_pr[id] = count
            total_count += count
        for id in background_pr.keys():
            background_pr[id] = background_pr[id]/total_count
    print('background model loaded!')
    return background_pr