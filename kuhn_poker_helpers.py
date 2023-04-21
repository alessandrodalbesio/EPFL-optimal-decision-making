import numpy as np
import cvxpy as cp
import pandas as pd
from itertools import product

# generate M matrix
def create_M():
    profiles_P1, profiles_P2 = create_profiles()
    M = np.nan*np.ones((len(profiles_P1),len(profiles_P2)))
    for p1_idx in range(len(profiles_P1)):
        for p2_idx in range(len(profiles_P2)):
            value = 0
            for C1_idx in range(3):
                C1 = ['J','Q','K'][C1_idx]
                for C2_idx in range(3):
                    if C1_idx==C2_idx:
                        continue
                    C2 = ['J','Q','K'][C2_idx]
                    # different outcomes
                    if (profiles_P1[p1_idx][C1] == 'check') and (profiles_P2[p2_idx][f'{C2}-checked'] == 'check'):
                        # check-check --> showdown
                        value += 1/6 if C1_idx>C2_idx else -1/6

                    if (profiles_P1[p1_idx][C1] == 'check') and (profiles_P2[p2_idx][f'{C2}-checked'] == 'bet'):
                        # check-raise
                        if profiles_P1[p1_idx][f'{C1}-raised'] == 'fold':
                            # P1 folds
                            value += -1/6
                        if profiles_P1[p1_idx][f'{C1}-raised'] == 'call':
                            # P2 calls --> showdown
                            value += 2/6 if C1_idx>C2_idx else -2/6

                    if (profiles_P1[p1_idx][C1] == 'bet') and (profiles_P2[p2_idx][f'{C2}-bet'] == 'fold'):
                        # bet-fold
                        value += 1/6

                    if (profiles_P1[p1_idx][C1] == 'bet') and (profiles_P2[p2_idx][f'{C2}-bet'] == 'call'):
                        # bet-call --> showdown
                        value += 2/6 if C1_idx>C2_idx else -2/6
            M[p1_idx,p2_idx] = value
    return M

def create_profiles():
    # generate profiles for P1:
    profiles_P1 = []
    for aJ, aQ, aK in product(['check','bet'], ['check','bet'], ['check','bet']):
        a2Js = [None] if aJ == 'bet' else ['fold', 'call'] # allowed to raise?
        a2Qs = [None] if aQ == 'bet' else ['fold', 'call'] # allowed to raise?
        a2Ks = [None] if aK == 'bet' else ['fold', 'call'] # allowed to raise?
        for a2J, a2Q, a2K in product(a2Js, a2Qs, a2Ks):
            profiles_P1.append(
                {
                    'J' : aJ,
                    'Q' : aQ,
                    'K' : aK,
                    'J-raised': a2J,
                    'Q-raised': a2Q,
                    'K-raised': a2K
                }
            )

    # generate profiles for P2:
    profiles_P2 = []
    for aJb, aQb, aKb, aJc, aQc, aKc in product(['fold','call'], ['fold','call'], ['fold','call'],['check','bet'],['check','bet'],['check','bet']):
        profiles_P2.append(
            {
            'J-checked' : aJc,
            'Q-checked' : aQc,
            'K-checked' : aKc,
            'J-bet': aJb,
            'Q-bet': aQb,
            'K-bet': aKb
            }
        )
    return profiles_P1, profiles_P2