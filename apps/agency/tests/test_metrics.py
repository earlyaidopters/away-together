from travel_lab.metrics import summarise

def test_failures_remain_in_accuracy_denominator():
    a={'field':'t','labels':['a','b'],'gold':0,'pred':0,'probabilities':[.8,.2]}
    b={'field':'t','labels':['a','b'],'gold':1,'pred':None,'probabilities':None}
    r=summarise([{'decisions':[a,b],'elapsed_ms':10,'error':'partial'}])
    assert r['accuracy']==.5;assert r['failed_decisions']==1;assert r['all_correct_rate']==0
    assert abs(r['brier_success_only']-.08)<1e-6
