class Apriori(object):
    def __init__(self, data, min_sup=2, min_conf=50):
        self.data = data
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.support_hash = {}

    def pruning(self, L):
        '''剪枝'''
        L_prune = []
        for item in L:
            support = sum(1 for transaction in self.data if item.issubset(transaction)) / len(self.data) * 100
            if support >= self.min_sup:
                L_prune.append(item)
                self.support_hash[item] = support
        return L_prune
    
    def frequent_itemsets_L1(self):
        '''创建单项频繁项集L1'''
        C1 = []  
        for transaction in self.data:  
            for item in transaction:  
                if [item] not in C1: 
                    C1.append([item])  
        C1 = [frozenset(item) for item in C1]
        L1 = self.pruning(C1)
        L1.sort()
        return L1
    
    def frequent_itemsets_Lk(self, L):
        '''根据频繁项集Lk-1创建频繁项集Lk'''
        Ck = []
        k = len(L[0])
        for itemset1 in L:
            for itemset2 in L:
                if itemset1 != itemset2:
                    union = itemset1 | itemset2
                    if len(union) == k+1 and union not in Ck:
                        Ck.append(union)
        Ck = [frozenset(item) for item in Ck]
        Lk = self.pruning(Ck)
        Lk.sort()
        return Lk

    def apriori(self):
        '''Apriori算法'''
        L = []
        Lk = self.frequent_itemsets_L1()
        while len(Lk) > 0:
            L += Lk
            Lk = self.frequent_itemsets_Lk(Lk)
        return L

    def association_rules(self, L):
        '''生成强关联规则'''
        rules = []
        for item1 in L:
            for item2 in L:
                if item1 != item2 and item1.issubset(item2):
                        confidence = self.support_hash[item2] / self.support_hash[item1] * 100
                        if confidence >= self.min_conf:
                            rules.append((item1, item2 - item1, confidence))
        return rules