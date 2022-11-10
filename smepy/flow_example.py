import struct_case as sc
import sme
import reader

def main():
    sc.declare_nary("and")
    name, facts = reader.read_meld_file('examples/domains_final/gripper_pg3.meld')
    water_flow = sc.StructCase(facts, name)
    name, facts = reader.read_meld_file('examples/domains_final/ferry_pg3.meld')
    heat_flow = sc.StructCase(facts, name)

    sme_1 = sme.SME(water_flow, heat_flow, max_mappings=5)
    gms = sme_1.match()
    for gm in gms:
        print(gm.entity_matches())
        print(gm.score)
        print("\n")

if __name__ == '__main__':
    main()
    
