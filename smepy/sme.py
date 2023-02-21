import smepy.struct_case as sc
import copy
import itertools

class SME:
    """The main class that holds all
    the information of a structure mapping process."""
    def __init__(self, base, target, max_mappings=3, forced_matches=None):
        self.base = base
        self.target = target
        self.max_mappings = max_mappings
         # a dict with base -> target  matches that should be forced
        self.force_matches = {} if forced_matches is None else {sc.Entity(k): sc.Entity(v) for k,v in forced_matches.items()} 


    def match(self):
        matches = create_all_possible_matches(self.base, self.target, self.force_matches)
        connect_matches(matches) 
        matches = decouple_matches(matches)
        valid_matches = consistency_propagation(matches)
        structural_evaluation(valid_matches)
        kernel_mappings = find_kernel_mappings(valid_matches) # kernel mappings are all root expressions
        global_mappings = greedy_merge(kernel_mappings, self.max_mappings)
        return global_mappings

class Mapping:
    """ """
    def __init__(self, matches=None):
        self.base_to_target = {}
        self.target_to_base = {}
        self.matches = set()
        self.score = 0.0
        if matches:
            self.add_all(matches)

    def get_mapped_base(self, base):
        if base in self.base_to_target:
            return self.base_to_target[base]
        else:
            return None

    def get_mapped_target(self, target):
        if target in self.target_to_base:
            return self.target_to_base[target]
        else:
            return None

    def is_consistent_with(self, match):
        base = match.base
        target = match.target
        corresponding_target = self.get_mapped_base(base)
        corresponding_base = self.get_mapped_target(target)
        is_base_consistent = (not corresponding_target) or \
            (corresponding_target == target)
        is_target_consistent = (not corresponding_base) or \
            (corresponding_base == base)
        return is_base_consistent and is_target_consistent
        
    def mutual_consistent(self, mapping):
        for match in mapping.matches:
            if not self.is_consistent_with(match):
                #print 'Mapping is not consistent with', match
                return False
        return True 
    
    def add(self, match, check_consistency=True):
        if match in self.matches:
            return 
        elif (not check_consistency) or self.is_consistent_with(match):
            base = match.base
            target = match.target
            self.base_to_target[base] = target
            self.target_to_base[target] = base
            self.matches.add(match)
        else:
            print('Mapping is not consistent with', match)
            raise ValueError

    def add_all(self, matches, check_consistency=True):
        for match in matches:
            self.add(match, check_consistency)

    def merge(self, mapping):
        # consistency should be checked before merging
        self.add_all(mapping.matches, check_consistency=False) 

    def evaluate(self):
        self.score = 0.0
        for match in self.matches:
            self.score += match.score
        return self.score

    def copy(self):
        new_mapping = Mapping(self.matches)
        new_mapping.score = self.score
        return new_mapping

    def entity_matches(self):
        entity_matches = []
        for match in self.matches:
            if isinstance(match.base, sc.Expression):
                pass
            elif isinstance(match.base, sc.Entity):
                entity_matches.append(match)
        return entity_matches  

    def expression_matches(self):
        entity_matches = []
        for match in self.matches:
            if isinstance(match.base, sc.Expression):
                entity_matches.append(match)
            elif isinstance(match.base, sc.Entity):
                pass
        return entity_matches  


    def __str__(self):
        entity_matches = []
        expression_matches = []
        for match in self.matches:
            if isinstance(match.base, sc.Expression):
                expression_matches.append(match)
            elif isinstance(match.base, sc.Entity):
                entity_matches.append(match)
        expression_matches_str = \
            ',\n'.join(map(repr, expression_matches))
        entity_matches_str = ', '.join(map(repr, entity_matches))
        return 'expression mappings:\n' + expression_matches_str + \
            '\n' + 'entity mappings:\n' + entity_matches_str    
        
class Match:
    """ """
    def __init__(self, base, target, score=0.0, instance_counter=1):
        self.base = base
        self.target = target
        self.score = score
        self.children = []
        self.parents = []
        self.mapping = None
        self.is_incomplete = False
        self.is_inconsistent = False
        self.is_commutative = False # if true, then there are multiple candidates for each child
        self.instance = instance_counter
        self.is_nary = len(base.args) != len(target.args) if isinstance(base, sc.Expression) else False
        
    def add_parent(self, parent):
        self.parents.append(parent)

    def remove_parent(self, parent):
        self.parents.remove(parent)

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)
        
    def local_evaluation(self):
        if isinstance(self.base, sc.Expression):
            self.score = predicate_match_score(self.base.predicate,
                                               self.target.predicate)
        else:
            self.score = 0.0
        return self.score

    def copy(self):
        nm = Match(self.base, self.target)
        nm.score = self.score
        nm.children = self.children
        nm.parents = self.parents
        nm.mapping = self.mapping
        nm.is_incomplete = self.is_incomplete
        nm.is_inconsistent = self.is_inconsistent
        nm.is_commutative = self.is_commutative
        nm.instance = self.instance

        return nm

        
    def __repr__(self):
        return '('+repr(self.base)+' -- '+repr(self.target)+')' + '[' + repr(self.instance) + ']'    

    def __eq__(self, other):
        return isinstance(other, Match) and\
            (self.base == other.base) and \
            (self.target == other.target) and \
            (self.instance == other.instance)

    def __hash__(self):
        return hash(repr(self))

    
class Params:
    """ """
    pass

def predicate_match_score(pred_1, pred_2):
    if pred_1.predicate_type == 'relation':
        if pred_1.name == pred_2.name:
            return 0.005
    elif pred_1.predicate_type == 'function':
        return 0.002
    else:
        return 0.0

def are_predicates_matchable(pred_1, pred_2):
    """
        Predicates are matchable if 
            - they are both functions
            - relations with the same name
    """
    if pred_1.predicate_type != pred_2.predicate_type:
        return False
    elif pred_1.predicate_type == 'relation':
        return pred_1.name == pred_2.name
    else:
        return True

def are_matchable(item_1, item_2, forced_matches):
    """
        Two items are matchable if
            - both are expressions and their predicates are matchable
            - both are entities
    """
    is_exp_1 = isinstance(item_1, sc.Expression)
    is_exp_2 = isinstance(item_2, sc.Expression)
    if is_exp_1 and is_exp_2:
        return are_predicates_matchable(item_1.predicate,
                                        item_2.predicate)
    elif (not is_exp_1) and (not is_exp_2):
        # return True if item_1 doesn't have a required match, otherwise check the required match
        return True if item_1 not in forced_matches else forced_matches[item_1] == forced_matches[item_2]

    else:
        return False
    
# need to change the pair stuff into match stuff
#TODO: add a possibility to pass a filter function as in SME
def create_all_possible_matches(case_1, case_2, forced_matches):
    """
        Constructs possible match as a cross product of all items
        for every pair, it checks whether it is a possible match
    """
    exp_list_1 = case_1.expression_list
    exp_list_2 = case_2.expression_list
    matches = set()
    for exp_1 in exp_list_1:
        for exp_2 in exp_list_2:
            new_matches = match_expression(exp_1, exp_2, forced_matches)
            matches = set.union(matches, new_matches)

    # if forced matches are provided, check they they are all fulfilled
    if len(forced_matches) > 0:
        tmp_forced_matches = copy(forced_matches)
        for item in matches:
            if isinstance(item.base, sc.Entity) and item.base in tmp_forced_matches:
                del tmp_forced_matches[item.base]

        # if anything is left in tmp_forced_matches, that means we haven't matched something
        if len(tmp_forced_matches) > 0:
            raise Exception(f"Not every forced match was possible: {tmp_forced_matches}")

    return sorted(matches, key=str)
    
def match_expression(exp_1, exp_2, forced_matches):
    """
        Match the two expressions and their arguments (not predicates)
    """
    pred_1 = exp_1.predicate
    pred_2 = exp_2.predicate
    args_1 = exp_1.args
    args_2 = exp_2.args
    pair_list = [(exp_1, exp_2)] + list(zip(args_1, args_2))
    if all([are_matchable(pair[0], pair[1], forced_matches) for pair in pair_list]):
        match_list = [Match(pair[0], pair[1]) for pair in pair_list]
        return set(match_list)
    else:
        return set()

def connect_matches(matches):
    """
        This connects the matches such that an expression is a parent of its arguments

        % commutativity enters here: a commutative predicate can match arguments in any order
        % n-ary-ness also enters here: we treat it as a commutative 
    """
    match_dict = {}
    for match in matches:
        match_dict[(match.base, match.target)] = match
    for match in matches:
        base = match.base
        target = match.target
        if isinstance(base, sc.Expression):
            if not (base.predicate.is_commutative() or target.predicate.is_commutative()):
                # if no involved predicates are commutative, do arg-by-arg match
                arg_pair_list = zip(base.args, target.args)
            else:
                # if at least one predicate is commutative, do the cross product of args
                arg_pair_list = [(x,y) for x in base.args for y in target.args]
                match.is_commutative = True

            for arg_pair in arg_pair_list:
                if arg_pair in match_dict:
                    child_match = match_dict[arg_pair]
                    child_match.add_parent(match)
                    match.add_child(child_match)
                else:
                    match.is_incomplete = True

def needs_refinement(cmatch, substitutions):
    """
        A match needs refinement if any of its children need refinement
    """
    return any([c in substitutions for c in cmatch.children])

def inspect_matches(matches):
    for ind, item in enumerate(matches): print(ind,": ", item, "\n\t", "\n\t".join([str(x) for x in item.children]))


def decouple_matches(matches):
    """
        Turns a match graph in with a match can have potentially multiple children for the same argument
            into a graph that has only one child per argument
    """
    match_graph = dict([(match, match.children) for match in matches])
    ordered_from_leaves_matches = topological_sort(match_graph) # ordered from leaves to roots

    new_matches = []  # new matches that will be returned
    substitutions = {}   # re-representation of matches
    refinements = {}  # matches that have been split

    for match in ordered_from_leaves_matches:
        if match.is_commutative or needs_refinement(match, refinements):
            # if the match is commutative
            child_groups = {}
            for child in match.children:
                # this check is needed for nary predicates -- we want to match all arguments of the smaller expression, therefore we organise the children according to the target elements
                k = child.target if (isinstance(match.base, sc.Expression) and len(match.base.args) > len(match.target.args)) else child.base

                if child in refinements:
                    child_groups[k] = child_groups.get(k, []) + refinements[child]
                else:
                    child_groups[k] = child_groups.get(k, []) + [child]

            variants = []

            #xx = list(child_groups.values())
            xx = sorted(child_groups.values(), key=str)

            for ind, children in enumerate(itertools.product(*xx)):
                nm = match.copy()
                nm.instance = ind + 1
                nm.children = [substitutions[c] for c in children]
                nm.parents = []
                variants.append(nm)

                # connect children
                for ch in nm.children:
                    ch.add_parent(nm)

            refinements[match] = variants
            for v in variants:
                substitutions[v] = v # for sake of easier retrieval later on

            new_matches = new_matches + variants
        else:
            # make a copy and add to new matches
            #  map the children and remove the parents (those will be added later)
            nm = match.copy()
            nm.parents = [] # will be added laster
            nm.children = [substitutions[c] for c in match.children]
            substitutions[match] = nm

            # connect the parent relation to children
            for ch in nm.children:
                ch.add_parent(nm)

            new_matches.append(nm)

    return new_matches

def consistency_propagation(matches):
    """
    This creates a full mapping of a root expressions/kernels. These might not be complete -- they might not have all constants/entities of the domains
    """
    match_graph = dict([(match, match.children) for match in matches])
    ordered_from_leaves_matches = matches #topological_sort(match_graph) # ordered from leaves to roots
    
    for match in ordered_from_leaves_matches:
        match.mapping = Mapping([match])
        for child in match.children:
            if match.mapping.mutual_consistent(child.mapping):
                match.mapping.merge(child.mapping)
            else:
                match.is_inconsistent = True
                break
    valid_matches = [match for match in ordered_from_leaves_matches \
                     if (not (match.is_incomplete or
                              match.is_inconsistent))]
    return valid_matches

def structural_evaluation(matches, trickle_down_factor=16):
    """
        Evaluates all found matches so far; computes the scores
    """
    #assume matches are still topologically sorted,
    #otherwise should sort it first
    for match in matches:
        match.local_evaluation()
    ordered_from_root_matches = matches[::-1] # this inverts the topological sort so that the first expressions are the most complciated ones

    for match in ordered_from_root_matches:
        for child in match.children:
            child.score += match.score * trickle_down_factor # propagates the score from parent to children
            if child.score > 1.0:
                child.score = 1.0
    
    for match in ordered_from_root_matches:
        match.mapping.evaluate() # sum of scores of all matches within a mapping

    return matches

def find_kernel_mappings(valid_matches):
    """
        Finds the kernels -- root expressions and their corresponding mapping
    """
    root_matches = []
    for match in valid_matches:
        are_parents_valid = [not (parent in valid_matches) \
                             for parent in match.parents]
        if all(are_parents_valid):
            root_matches.append(match)
    return [match.mapping.copy() for match in root_matches]

def greedy_merge(kernel_mappings, num_mappings):
    sorted_k_mapping_list = sorted(kernel_mappings,
                                   key=(lambda mapping: mapping.score),
                                   reverse=True)
    global_mappings = []
    max_score = 0.0
    while (len(global_mappings) < num_mappings) and \
          (len(sorted_k_mapping_list) > 0):
        global_mapping = sorted_k_mapping_list[0]
        sorted_k_mapping_list.remove(global_mapping)
        
        for kernel_mapping in sorted_k_mapping_list[:]:
            if global_mapping.mutual_consistent(kernel_mapping):
                global_mapping.merge(kernel_mapping)
                sorted_k_mapping_list.remove(kernel_mapping)
        
        score = global_mapping.evaluate()
        if score <= 0.8 * max_score:
            break
        elif score > max_score:
            max_score = score
        global_mappings.append(global_mapping)
    
    global_mappings.sort(key=lambda mapping: mapping.score, \
                         reverse=True)
    return global_mappings

def topological_sort(graph_dict):
    """Input: graph represented as
    {node: [next_node_1, next_nodet_2], ...}"""
    sorted_list = []
    sorted_set = set()
    new_graph_dict = graph_dict.copy()
    while new_graph_dict:
        for node in new_graph_dict:
            next_node_list = new_graph_dict[node]
            if all([(next_node in sorted_set) \
                    for next_node in next_node_list]):
                sorted_list.append(node)
                sorted_set.add(node)
                del new_graph_dict[node]
                break
        else:
            print('Cyclic graph!')
            return
    return sorted_list    
