from travel_lab.catalogue import verdict,catalogue

def answers(choice=0,confidence=.95):
    p=[(1-confidence)/2]*3;p[choice]=confidence
    return [{'id':t,'choice':choice,'probabilities':p} for t in ['refund','arrival','facility','activity']]
def test_budget_boundary_and_review():
    c=catalogue();offer=c['offers'][0];p={'budget':1290,'requirements':['refund']}
    assert verdict(p,offer,answers(),.8)['status']=='match'
    p['budget']=1289
    assert verdict(p,offer,answers(),.8)['status']=='decline'
    p['budget']=1290
    assert verdict(p,offer,answers(2),.8)['status']=='review'
    assert verdict(p,offer,answers(0,.6),.8)['status']=='review'
def test_unknown_currency_never_assumed():
    c=catalogue();offer=c['offers'][0].copy();offer['currency']='GBP'
    assert verdict(c['profiles'][0],offer,answers(),.8)['status']=='review'
def test_failure_dominates_unknown():
    c=catalogue();p={'budget':1,'requirements':['refund']}
    assert verdict(p,c['offers'][0],answers(2),.8)['status']=='decline'
