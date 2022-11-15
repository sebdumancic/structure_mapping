import smepy

def compare(act1, act2):
    for e, a in zip(act1, act2):
        print(e, "\n|||\n", a, "\n")
    

smepy.declare_nary('and')
base = [
    ['action', 
        'move', 
        ['precon', ['and', ['term1', 'room', 'move-from'], ['term1', 'room', 'move-to'], ['term1', 'at-robby', 'move-from']]], 
        ['effects', ['and', ['term1', 'at-robby', 'move-to'], ['not', ['term1', 'at-robby', 'move-from']]]]], 
    ['action', 
        'pick', 
        ['precon', ['and', ['term1', 'ball', 'pick-obj'], ['term2', 'at', 'pick-obj', 'pick-room'], ['term1', 'room', 'pick-room'], ['term1', 'at-robby', 'pick-room'], ['term1', 'gripper', 'pick-gripper'], ['term1', 'free', 'pick-gripper']]], 
        ['effects', ['and', ['term2', 'carry', 'pick-obj', 'pick-gripper'], ['not', ['term1', 'free', 'pick-gripper']], ['not', ['term2', 'at', 'pick-obj', 'pick-room']]]]], 
    ['action', 
        'drop', 
        ['precon', ['and', ['term1', 'room', 'drop-room'], ['term1', 'gripper', 'drop-gripper'], ['term1', 'ball', 'drop-obj'], ['term2', 'carry', 'drop-obj', 'drop-gripper'], ['term1', 'at-robby', 'drop-room']]], 
        ['effects', ['and', ['term2', 'at', 'drop-obj', 'drop-room'], ['term1', 'free', 'drop-gripper'], ['not', ['term2', 'carry', 'drop-obj', 'drop-gripper']]]]]
    ]
target = [
    ['action', 
        'sail', 
        ['precon', ['and', ['term1', 'location', 'sail-from'], ['term2', 'not-eq', 'sail-from', 'sail-to'], ['term1', 'at-ferry', 'sail-from'], ['term1', 'location', 'sail-to']]], 
        ['effects', ['and', ['term1', 'at-ferry', 'sail-to'], ['not', ['term1', 'at-ferry', 'sail-from']]]]],
    ['action', 
        'board', 
        ['precon', ['and', ['term1', 'car', 'board-car'], ['term1', 'location', 'board-loc'], ['term2', 'at', 'board-car', 'board-loc'], ['term1', 'at-ferry', 'board-loc'], ['term0', 'empty-ferry']]], 
        ['effects', ['and', ['term1', 'on', 'board-car'], ['not', ['term2', 'at', 'board-car', 'board-loc']], ['not', ['term0', 'empty-ferry']]]]], 
    ['action', 
        'debark', 
        ['precon', ['and', ['term1', 'car', 'debark-car'], ['term1', 'location', 'debark-loc'], ['term1', 'at-ferry', 'debark-loc'], ['term1', 'on', 'debark-car']]], 
        ['effects', ['and', ['term2', 'at', 'debark-car', 'debark-loc'], ['term0', 'empty-ferry'], ['not', ['term1', 'on', 'debark-car']]]]], 
    ]

base_sc = smepy.StructCase(base, 'base')
target_sc = smepy.StructCase(target, 'target')

#import ipdb; ipdb.set_trace()
# name, facts = smepy.read_meld_file('domains_final/gripper_pg3.meld')
# base_alt = smepy.StructCase(facts, name)

# name, facts = smepy.read_meld_file('domains_final/ferry_pg3.meld')
# target_alt = smepy.StructCase(facts, name)

base_pr = [['action', 'move', ['precon', ['and', ['term1', 'at-robby', 'move-from'], ['term1', 'room', 'move-to'], ['term1', 'room', 'move-from']]], ['effects', ['and', ['term1', 'at-robby', 'move-to'], ['not', ['term1', 'at-robby', 'move-from']]]]], ['action', 'pick', ['precon', ['and', ['term1', 'free', 'pick-gripper'], ['term1', 'room', 'pick-room'], ['term1', 'gripper', 'pick-gripper'], ['term2', 'at', 'pick-obj', 'pick-room'], ['term1', 'at-robby', 'pick-room'], ['term1', 'ball', 'pick-obj']]], ['effects', ['and', ['term2', 'carry', 'pick-obj', 'pick-gripper'], ['not', ['term1', 'free', 'pick-gripper']], ['not', ['term2', 'at', 'pick-obj', 'pick-room']]]]], ['action', 'drop', ['precon', ['and', ['term1', 'room', 'drop-room'], ['term1', 'gripper', 'drop-gripper'], ['term2', 'carry', 'drop-obj', 'drop-gripper'], ['term1', 'at-robby', 'drop-room'], ['term1', 'ball', 'drop-obj']]], ['effects', ['and', ['term1', 'free', 'drop-gripper'], ['term2', 'at', 'drop-obj', 'drop-room'], ['not', ['term2', 'carry', 'drop-obj', 'drop-gripper']]]]]]
base_predicators = smepy.StructCase(base_pr, 'gripper-predicators')

target_pr = [['action', 'board', ['precon', ['and', ['term1', 'location', 'board-loc'], ['term0', 'empty-ferry'], ['term1', 'car', 'board-car'], ['term1', 'at-ferry', 'board-loc'], ['term2', 'at', 'board-car', 'board-loc']]], ['effects', ['and', ['term1', 'on', 'board-car'], ['not', ['term2', 'at', 'board-car', 'board-loc']], ['not', ['term0', 'empty-ferry']]]]], ['action', 'debark', ['precon', ['and', ['term1', 'on', 'debark-car'], ['term1', 'car', 'debark-car'], ['term1', 'at-ferry', 'debark-loc'], ['term1', 'location', 'debark-loc']]], ['effects', ['and', ['term2', 'at', 'debark-car', 'debark-loc'], ['term0', 'empty-ferry'], ['not', ['term1', 'on', 'debark-car']]]]], ['action', 'sail', ['precon', ['and', ['term1', 'at-ferry', 'sail-from'], ['term2', 'not-eq', 'sail-from', 'sail-to'], ['term1', 'location', 'sail-from'], ['term1', 'location', 'sail-to']]], ['effects', ['and', ['term1', 'at-ferry', 'sail-to'], ['not', ['term1', 'at-ferry', 'sail-from']]]]]]
target_predicators = smepy.StructCase(target_pr, 'ferry-predicators')



sme_1 = smepy.SME(base_sc, target_sc, max_mappings=5)
gms = sme_1.match()
for gm in gms:
    print("Entity mappings:")
    for ind, item in enumerate(gm.entity_matches()): print(ind, ": ", item)
    # print("Expressions mappings:")
    # for ind, item in enumerate(gm.expression_matches()): print(ind, ": ", item)
    print(gm.score)
    print("\n")