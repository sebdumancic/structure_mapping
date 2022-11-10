import smepy

def main():
    smepy.declare_nary("and")
    name, facts = smepy.read_meld_file('water_flow.meld')
    water_flow = smepy.StructCase(facts, name)
    name, facts = smepy.read_meld_file('heat_flow.meld')
    heat_flow = smepy.StructCase(facts, name)

    sme_1 = smepy.SME(water_flow, heat_flow, max_mappings=5)
    gms = sme_1.match()
    for gm in gms:
        print("Entity mappings:")
        for ind, item in enumerate(gm.entity_matches()): print(ind, ": ", item)
        # print("Expressions mappings:")
        # for ind, item in enumerate(gm.expression_matches()): print(ind, ": ", item)
        print(gm.score)
        print("\n")

if __name__ == '__main__':
    main()
    
