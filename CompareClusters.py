from itertools import combinations
from math import factorial
from math import log
from math import sqrt


class CompareClusters:
    def __init__(self, vertices, cluster1, cluster2):
        self.x = vertices
        self.c1 = cluster1
        self.c2 = cluster2
        self.n = len(self.x)
        self.M = list()
        self.S = dict()
        self.N = dict()
        self.h1 = 0
        self.h2 = 0
        self.h12 = 0
        self.build_confusion_matrix()
        self.build_pair_matrix()
        self.fulfilling = False  # be very careful...

    def build_confusion_matrix(self):
        for cr1 in self.c1:
            r = list()
            for cr2 in self.c2:
                pij = len(set(cr1).intersection(set(cr2)))
                r.append(pij)
                if pij != 0:
                    self.h12 = self.h12 - (pij/self.n * log(pij/self.n, 2))
            self.M.append(r)

    def build_pair_matrix(self):
        s11 = list()
        s00 = list()
        s10 = list()
        s01 = list()
        cs = combinations(self.x, 2)
        for a in cs:
            # for each pair, check if they are in the same cluster or not...
            sameclusterin1 = False
            sameclusterin2 = False
            for ci in self.c1:
                if a[0] in ci and a[1] in ci:
                    sameclusterin1 = True
            for cj in self.c2:
                if a[0] in cj and a[1] in cj:
                    sameclusterin2 = True

            if sameclusterin1 and sameclusterin2:
                s11.append(a)
            elif not sameclusterin1 and not sameclusterin2:
                s00.append(a)
            elif sameclusterin1 and not sameclusterin2:
                s10.append(a)
            elif not sameclusterin1 and sameclusterin2:
                s01.append(a)
        self.S["s11"] = s11
        self.S["s00"] = s00
        self.S["s10"] = s10
        self.S["s01"] = s01
        self.N["n11"] = len(s11)
        self.N["n00"] = len(s00)
        self.N["n10"] = len(s10)
        self.N["n01"] = len(s01)
        # compute the entropies
        for cr1 in self.c1:
            p = len(cr1) / self.n
            self.h1 = self.h1 - (p * log(p, 2))
        for cr2 in self.c2:
            p = len(cr2) / self.n
            self.h2 = self.h2 - (p * log(p, 2))

    def chi_squared_coefficient(self):
        chi = 0
        ci = 0
        for cr1 in self.c1:
            cj = 0
            for cr2 in self.c2:
                e = (len(cr1)*len(cr2))/self.n
                chi = chi + pow((self.M[ci][cj] - e), 2)/e
                cj = cj + 1
            ci = ci + 1
        return chi

    def general_rand_index(self):
        return (2*(self.N["n11"] + self.N["n00"]))/(self.n * (self.n-1))

    def cnr(self, n, r):
        if n < r:
            return 0
        if n == r:
            return 1
        if r == 1:
            return n
        return factorial(n) / (factorial(r) * factorial(n-r))

    def adjusted_rand_index(self):
        t1 = 0
        for cr1 in self.c1:
            t1 = t1 + self.cnr(len(cr1), 2)
        t2 = 0
        for cr2 in self.c2:
            t2 = t2 + self.cnr(len(cr2), 2)
        t3 = (2*t1*t2)/(self.n*(self.n-1))

        r = 0
        ci = 0
        for cr1 in self.c1:
            cj = 0
            for cr2 in self.c2:
                r = r + self.cnr(self.M[ci][cj], 2)
                cj = cj + 1
            ci = ci + 1
        return (r - t3) / (((t1+t2)/2) - t3)

    def jaccard_index(self):
        return self.N["n11"] / (self.N["n11"] + self.N["n10"] + self.N["n01"])

    def mutual_information(self):
        mi = 0
        ci = 0
        for cr1 in self.c1:
            cj = 0
            pi = len(cr1) / self.n
            for cr2 in self.c2:
                pj = len(cr2) / self.n
                pij = self.M[ci][cj] / self.n
                if pij > 0:  # log raises an exception if pij == 0
                    mi = mi + (pij * log((pij/(pi*pj)), 2))
                cj = cj + 1
            ci = ci + 1
        return mi

    def normalized_mutual_information(self):
        return self.mutual_information() / (sqrt(self.h1*self.h2))

    def normalized_mutual_information_by_fred_jain(self):
        return 2 * self.mutual_information() / (self.h1 + self.h2)

    def normalized_mutual_information_by_danon(self):
        return (self.h1 + self.h2 - self.h12) / ((self.h1 + self.h2) / 2)

    def variation_of_information(self):
        return self.h1 + self.h2 - 2*self.mutual_information()

    def normalized_variation_of_information(self):
        h_x_given_y = self.h12 - self.h2
        h_y_given_x = self.h12 - self.h1
        return 0.5 * ((h_x_given_y / self.h1) + (h_y_given_x / self.h2))

    def h(self, p):
        if p <= 0:
            return 0
        return -1 * p * log(p, 2)

    def h_xk_yl(self, xk, yl):
        sk = set(xk)
        sl = set(yl)
        p11 = len(sk.intersection(sl)) / self.n
        p10 = (len(sk) - len(sk.intersection(sl))) / self.n
        p01 = (len(sl) - len(sk.intersection(sl))) / self.n
        p00 = (self.n - len(sk.union(sl))) / self.n
        pl1 = len(yl) / self.n
        pl0 = 1 - (len(yl) / self.n)
        if self.h(p11) + self.h(p00) > self.h(p01) + self.h(p10):
            self.fulfilling = True
        else:
            self.fulfilling = False
        return self.h(p11) + self.h(p00) + self.h(p01) + self.h(p10) - self.h(pl1) - self.h(pl0)

    def hxynorm(self, c1, c2):
        hlist = list()
        hxkyn = 0
        for cr1 in c1:
            hlist.clear()
            for cr2 in c2:
                hv = self.h_xk_yl(cr1, cr2)
                if self.fulfilling:
                    hlist.append(hv)
            # if the hlist is empty, then we use h(xk)
            pxk = len(cr1) / self.n
            hxk = self.h(pxk)
            if len(hlist) == 0:
                hxkyn = hxkyn + 1
            else:
                if hxk == 0:
                    print("DIVISION BY ZERO!!! Returning 0")
                else:
                    hxkyn = hxkyn + (min(hlist) / hxk)
        if len(c1)==0: return 0
        return hxkyn / len(c1)

    def nvi_overlapping(self):
        if len(self.c1) == 1 or len(self.c2) == 1:
            return 0
        return 1 - (0.5 * (self.hxynorm(self.c1, self.c2) + self.hxynorm(self.c2, self.c1)))
