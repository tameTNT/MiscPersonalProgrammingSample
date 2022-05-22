# Copy of code written for SAT solving coursework in Computational Thinking Module at Durham University
# Received 68/76 total marks (all lost on efficiency of unit_propagate, pure_literal_eliminate and dpll_sat_solve)

import copy
import re
from collections import Counter
from typing import List, Set, Iterator, Iterable, Dict, Union


# import time
# from tqdm import trange


# === OWN HELPER FUNCTIONS ===
def sort_literals(literal_iterable: Iterable[int]) -> List[int]:
    """
    Sorts the iterable of literals given by each literal's absolute value (i.e. ignoring negation).
    This is most useful for readability and for ensuring consistent ordering in other functions.

    e.g. ``sort_literals([3, -2, -1]) == [-1, -2, 3]``
    """

    return sorted(list(literal_iterable), key=lambda x: abs(x))


def extract_variables(clause_set: List[List[int]], clean: bool = True) -> List[int]:
    """
    Extracts a sorted list of all unique variables from clause_set.

    e.g. ``extract_variables([[-1], [-2, 1], [3]]) == [1, 2, 3]``

    If clean is False, then the above would return ``[-1, -2, 1, 3]``.
    In this case, negated values are treated as unique and the output is not sorted.
    """

    literals = [literal for clause in clause_set for literal in clause]  # flatten clause_set
    if clean:
        literals = set(map(abs, literals))  # remove duplicates and remove negations
        literals = list(literals)  # sort_literals(literals)
    else:
        literals = set(literals)
    return literals


def max_occurrence_literal(clause_set: List[List[int]]) -> int:
    """
    Returns the literal most commonly occurring in clause_set
    """
    literals = [literal for clause in clause_set for literal in clause]  # flatten clause_set
    return Counter(literals).most_common(1)[0][0]  # select the 1 most common literal


# def moms(clause_set: List[List[int]]) -> int:
#     """
#     Returns the MOMS (Maximum Occurrence in clauses of Minimum Size) literal in clause_set
#     """
#     min_clauses = []
#     min_length = -1
#     for clause in clause_set:
#         clause_len = len(clause)
#         if clause_len < min_length or min_length == -1:
#             min_clauses.append(clause)
#             min_length = clause_len
#
#     return max_occurrence_literal(min_clauses)


def propagate_assignment(clause_set: List[List[int]], assignment: int) -> List[List[int]]:
    """
    Propagates the variable assignment through clause_set to return a new clause_set.

    e.g. ``propagate_assignment([[1, 2], [-1, -2]], 1) == [[-2]]``

    Note that this can generate [[]+] (i.e. only unsatisfiable empty clauses remain) (F = [∅])

    e.g. ``propagate_assignment([[1], [1]], -1) == [[], []]``
    """

    # create a deep copy since this is a nested list, and we don't want to modify in-place
    new_clause_set = copy.deepcopy(clause_set)

    sat_clause_indices = list()  # keep track of clauses that are satisfied by assignment
    for i, clause in enumerate(new_clause_set):
        clause_s = set(clause)  # speeds up lookups (in)
        if assignment in clause_s:  # this clause is guaranteed to be satisfied
            sat_clause_indices.append(i)  # add it to the removal list
        elif -assignment in clause_s:
            # remove all instances of this literal from the clause
            # since that literal will always be false under the assignment
            new_clause_set[i] = [literal for literal in clause_s if literal != -assignment]

    for satisfied_i in reversed(sat_clause_indices):  # go backwards so pop indices are correct
        # remove clauses satisfied by the assignment since these will now always be true
        new_clause_set.pop(satisfied_i)

    return new_clause_set


def generate_all_assignments(variables: List[int]) -> Iterator[Set[int]]:
    """
    A *generator* that yields sets of every possible truth assignment (2^[num variables])
     for the variables provided in variables. These are yielded as sets to speed up lookups (in)
    e.g. For variables=[1, 2], yields {1, 2}, {-1, 2}, {1, -2}, {-1, -2} in this order

    :param variables: List of literals to generate truth assignment permutations of.
    :return: An iterator object that produces sets of integers (possible truth assignments).
    """

    if len(variables) == 1:  # down to component part - yield each variation
        yield {variables[0]}
        yield {-variables[0]}
    elif len(variables) == 0:
        yield set()
    else:
        for back_half in generate_all_assignments(variables[1:]):
            yield {variables[0]}.union(back_half)
            yield {-variables[0]}.union(back_half)


def check_sat_assignment(clause_set: List[List[int]], assignment: List[int]) -> bool:
    """
    Confirms whether an assignment satisfies a clause set
    :param clause_set: Clause set to satisfy
    :param assignment: Literal assignment to test - possibly modulo pure and unit literals
    :return: True is clause_set is satisfied by assignment. False otherwise
    """

    for ass in assignment:
        clause_set = propagate_assignment(clause_set, ass)
    clause_set = unit_propagate(clause_set)
    clause_set = pure_literal_eliminate(clause_set)

    if len(extract_variables(clause_set)) == 0:
        return True
    else:
        return False


# === REQUIRED FUNCTIONS ===
def load_dimacs(filepath: str, print_comments: bool = False) -> List[List[int]]:
    """
    Write some Python code that loads a textual file in DIMACS format into an internal
    representation of a clause set, for which we will use a list of lists.
    For example, (v1 ∨ ¬v2) ∧ (¬v1 ∨ v3) would become [[1,−2], [−1, 3]].
    (Any line starting with a c is a comment.)
    [6 marks]

    :param filepath: The full name of the DIMACS file to load (e.g. "sample_SAT.txt").
        Can also include '/'s (e.g. "SAT/sample_SAT.txt")
    :param print_comments: If True, lines starting with c in the dimacs file are printed
    :return: A nested list representing a clause set - i.e. a list of clauses
    :raises FileNotFoundError: If no file was found at path filepath
    :raises Exception: If the file was found but there was error in parsing
        (e.g. missing or incorrect values for N/M)
    """

    try:
        with open(filepath, 'r') as fobj:
            n, m = 0, 0
            clause_set = list()
            for i, line in enumerate(fobj.readlines()):
                line = line.strip()  # remove leading and trailing whitespace
                if not line:  # if the line is blank, skip processing it
                    continue

                if line[0] == 'c':  # comment line
                    if print_comments:
                        print(f'[{i}] Comment: {line[1:]}')
                elif line[0] == 'p':  # header line at top of file
                    match = re.match(r'p cnf (\d+) +(\d+)', line)
                    if match:
                        n, m = map(int, match.groups())
                    else:
                        raise Exception(f'DIMACS file ({filepath}) is in an unexpected format. '
                                        f'Line {i+1} did not provide values '
                                        'for N and M as expected.')
                else:  # clause line
                    # line = line.removesuffix(' 0')
                    # clause = list(map(int, line.split(' ')))
                    clause = [int(x) for x in re.findall(r'(?!0)-?\d+', line)]

                    if clause:
                        max_literal = max(map(abs, clause))
                        if max_literal > n:
                            raise Exception(f'DIMACS file ({filepath}) is in an unexpected format. '
                                            f'Line {i+1} provided the literal {max_literal} which '
                                            f'was higher than the expected max given by N, {n}.')
                        clause_set.append(clause)

                    elif print_comments:
                        print(f'NB: No clause, header or comment was detected on line {i+1}.')

        if len(clause_set) == m:
            return clause_set
        else:
            raise Exception(f'The DIMACS file provided ({filepath}) claimed there were {m} total '
                            f'clauses (M) but {len(clause_set)} were found.')

    except FileNotFoundError:
        raise FileNotFoundError(f'"{filepath}" was not found in the current working directory')


def simple_sat_solve(clause_set: List[List[int]],
                     print_all: bool = False) -> Union[List[int], bool]:
    """
    Write a Python function simple sat solve in a single argument clause_set that solves
    the satisfiability of the clause set by running through all truth assignments. In case the
    clause set is satisfiable it should output a satisfying assignment. A full (truth) assignment
    should be represented by a list of literals. For example v1 ∧ ¬v2 ∧ v3 would be [1,−2, 3].
    [10 marks]

    :param clause_set: List of clauses to solve satisfiability of.
    :param print_all: Boolean specifying whether to print every assignment as it is found.
    :return: False if clause_set is not satisfiable. Otherwise, a satisfying truth assignment.
    """

    literals = extract_variables(clause_set)
    for assignment_set in generate_all_assignments(literals):
        # print(assignment_set)
        set_is_sat = True
        for clause in clause_set:
            clause_is_sat = False
            for literal in clause:
                if literal in assignment_set:
                    # only need one SAT literal per clause because each clause a disjunction
                    clause_is_sat = True
                    break
            if not clause_is_sat:
                set_is_sat = False  # all clauses must be SAT because conjunction
                break

        if set_is_sat:  # SAT
            if print_all:
                print(sort_literals(assignment_set))
            else:
                return list(assignment_set)

    return False  # UNSAT


def branching_sat_solve(clause_set: List[List[int]], partial_assignment: List[int],
                        initial: bool = True) -> Union[List[int], bool]:
    """
    Write a recursive Python function branching_sat_solve in the two arguments clause_set
    and partial_assignment that solves the satisfiability of the clause set by branching on the
    two truth assignments for a given variable. In case the clause set is satisfiable under the
    partial assignment it should output a satisfying assignment. When this is run with an empty
    partial assignment it should act as a SAT-solver. A partial assignment should be represented by
    a list of literals, as was a full assignment in the previous question.
    [10 marks]

    :param clause_set: List of clauses to solve satisfiability of.
    :param partial_assignment: A list of assignments to propagate through clause_set initially.
    :param initial: Do not change this default - it used by the function to skip propagating
        partial_assignment when this has already been done by definition in outer calls.
    :return: False if clause_set is unsatisfiable. Otherwise, a satisfying truth assignment.
    """

    if initial:  # clean up clause set if this is the initial call of the function
        for assignment in partial_assignment:  # iterates through all given assignments
            clause_set = propagate_assignment(clause_set, assignment)

    # NB: bool([[]]) == True
    #     bool([[], []]) == True
    #     bool([]) == False
    #     ∅ is the empty set
    variables = extract_variables(clause_set)  # clause_set is referred to as F from here on
    if not variables:  # variables == [] (var(F) = ∅)
        if not clause_set:  # F == [] i.e. no clauses left to satisfy remain (F = ∅)
            return partial_assignment  # SAT
        else:  # F == [[]+] i.e. only unsatisfiable empty clauses remain (F = [∅])
            return False  # UNSAT

    elif 0 in map(len, clause_set):  # F contains an unsatisfiable empty clause
        return False  # UNSAT

    else:  # there still exist variables and non-empty clauses in F
        x = clause_set[0][0]  # branch on first literal in clause set

        for literal in [x, -x]:  # branch on var as well as on -var in that order
            branch_partial_assignment = partial_assignment + [literal]
            new_clause_set = propagate_assignment(clause_set, literal)
            branch_result = branching_sat_solve(new_clause_set, branch_partial_assignment, False)
            if branch_result is not False:  # if branch_result is a satisfying assignment
                # is not False used because [] is a valid truth assignment but evaluates to False
                return branch_result  # SAT

        # implies x and -x branches are both False (i.e. UNSAT)
        return False  # so whole tree at this point is UNSAT


# def quad_unit_propagate(clause_set: List[List[int]]) -> List[List[int]]:
#     # OLD QUADRATIC (n^2) CODE (? - 8Queens takes 0.606)
#     def get_unit_literals(cs: List[List[int]]) -> List[int]:
#         """
#         Returns a list of all unit literals in the clause set cs
#
#         e.g. ``get_unit_literals([[1], [-2], [1, 2]]) == [1, -2]``
#         """
#
#         return [clause[0] for clause in cs if len(clause) == 1]
#
#     new_clause_set = clause_set
#
#     unit_literals = get_unit_literals(new_clause_set)
#     while unit_literals:
#         for literal in unit_literals:
#             new_clause_set = propagate_assignment(new_clause_set, literal)
#         unit_literals = get_unit_literals(new_clause_set)
#
#     return new_clause_set


def unit_propagate(clause_set: List[List[int]],
                   abort_on_contra: bool = False) -> Union[List[List[int]], str]:
    """
    Write a Python function unit propagate in a single argument clause_set which outputs
    a new clause set after iteratively applying unit propagation until it cannot be applied further.
    [10 marks]

    :param clause_set: Clause set to apply unit propagation to.
    :param abort_on_contra: If True, the function will immediately halt when an unsatisfiable clause
        (i.e. []) is formed by the unit propagation and return 'contradiction'
    :return: Clause set after unit propagation has been applied.
         I.e. all clauses of length 1 (e.g. [1]) are removed from the clause set
         and the deduced assignment propagated
    """

    # linear time algorithm (? - 8Queens takes 0.255)
    # implemented based on https://en.wikipedia.org/wiki/Unit_propagation#Complexity

    def add_key_val(dict_: Dict[int, list], key, val):
        if key in dict_:
            dict_[key].append(val)
        else:
            dict_[key] = [val]

    tracker: Dict[int, list] = dict()
    unit_literals = set()
    # iterate through all n literals in the clause set and note where each variable occurs
    for i, clause in enumerate(clause_set):
        if len(clause) == 1:  # unit clause
            literal = clause[0]
            unit_literals.add(literal)
            add_key_val(tracker, abs(literal), i)
        else:
            for literal in clause:
                add_key_val(tracker, abs(literal), i)

    # new_clause_set = copy.deepcopy(clause_set)  # we're allowed to work in-place
    clauses_to_remove = set()
    # work through clause set propagating unit literals until there are none left
    while unit_literals:
        literal_to_propagate = unit_literals.pop()  # pick any unit literal
        affected_clauses = tracker[abs(literal_to_propagate)]  # where does this variable occur?
        for clause_i in affected_clauses:
            if literal_to_propagate in clause_set[clause_i]:  # exact literal present...
                # (note that this includes the unit clauses themselves)
                clauses_to_remove.add(clause_i)  # so clause satisfied so mark for removal
            else:  # negation of literal present instead... just remove it
                new_clause = []
                remaining = 0  # count how many literals remain in clause after unit literal removal
                for literal in clause_set[clause_i]:
                    if literal != -literal_to_propagate:  # include all bar the negation of the unit
                        new_clause.append(literal)
                        remaining += 1
                clause_set[clause_i] = new_clause  # update original clause set with new clause

                if remaining == 1:  # in case a new unit clause has been formed
                    unit_literals.add(new_clause[0])
                elif remaining == 0 and abort_on_contra:  # a clause of length [] is a contradiction
                    return 'contradiction'  # abort immediately if abort_on_contra given

        tracker[abs(literal_to_propagate)] = []  # no instances of the variable should remain

    for clause_i in sorted(clauses_to_remove, reverse=True):  # go backwards so pop indices correct
        clause_set.pop(clause_i)  # actually remove all created unit clauses

    return clause_set


def pure_literal_eliminate(clause_set: List[List[int]]) -> List[List[int]]:
    """
    Write a Python function pure literal eliminate in a single argument clause set which
    outputs a new clause set after iteratively applying the pure literal assignment scheme until it
    cannot be applied further.
    [10 marks]

    :param clause_set: Clause set to apply pure literal elimination to.
    :return: Clause set after pure literal elimination has been applied iteratively.
        I.e. if a literal x is pure (only x appears in the clause set) then it is removed
        and the deduced assignment propagated.
    """

    # tracks whether -l and l have been seen
    literal_tracker = {variable: [False, False] for variable in extract_variables(clause_set)}

    for clause in clause_set:
        for literal in clause:  # update tracker for each variable
            literal_tracker[abs(literal)][literal > 0] = True

    pure_literals = set()
    for var, lit_status in literal_tracker.items():
        # all(status) => [True, True] => var and -var present
        if not all(lit_status):  # either both False or only one False
            if lit_status[0]:  # [True, False] => only -var present in clause_set
                pure_literals.add(-var)
            elif lit_status[1]:  # [False, True] => only var present in clause_set
                pure_literals.add(var)

    if pure_literals:
        # remove any clauses containing pure literals from the clause_set then re-detect any PLs
        # using set intersections is notably faster than verifying existence using in
        clause_set = [
            clause for clause in clause_set if not set(clause).intersection(pure_literals)
        ]
        return pure_literal_eliminate(clause_set)

    return clause_set


def dpll_sat_solve(clause_set: List[List[int]], partial_assignment: List[int], initial: bool = True,
                   use_max_heuristic: bool = True) -> Union[List[int], bool]:
    """
    Write a recursive Python function dpll sat solve in the two arguments clause set and
    partial assignment that solves the satisfiability of the clause set by applying unit propagation
    and pure literal elimination before branching on the two truth assignments for a given
    variable (this is the famous DPLL algorithm). In case the clause set is satisfiable under the
    partial assignment it should output a satisfying assignment. When this is run with an empty
    partial assignment it should act as a SAT-solver.
    [20 marks]

    :param clause_set: List of clauses to solve satisfiability of.
    :param partial_assignment: A list of assignments to propagate through clause_set initially.
    :param initial: Do not change this default - it used by the function to skip propagating
        partial_assignment when this has already been done by definition in outer calls.
    :param use_max_heuristic: If True, chooses the most common literal in the clause
        set each time to branch on. Otherwise, simply branches on the 1st literal in the clause set
    :return: False if clause_set is not satisfiable. Otherwise, a satisfying truth assignment
        MODULO PURE LITERALS AND UNIT CLAUSES.
    """

    if initial:
        for assignment in partial_assignment:
            clause_set = propagate_assignment(clause_set, assignment)

    # applies UP and PLE *in-place*
    if unit_propagate(clause_set, abort_on_contra=True) == 'contradiction':
        return False  # UNSAT - an unsatisfiable clause (i.e. []) was found in clause_set after UP
    pure_literal_eliminate(clause_set)

    variables = extract_variables(clause_set)
    if not variables:
        if not clause_set:
            return sort_literals(partial_assignment)  # SAT
        else:
            return False  # UNSAT
    # elif 0 in map(len, clause_set):  # F contains an unsatisfiable empty clause
    #     return False  # UNSAT
    else:
        if use_max_heuristic:
            x = max_occurrence_literal(clause_set)  # branch on most common literal
        else:
            x = clause_set[0][0]  # branch on first literal of clause set by default

        for literal in [x, -x]:
            branch_partial_assignment = partial_assignment + [literal]
            new_clause_set = propagate_assignment(clause_set, literal)
            branch_result = dpll_sat_solve(new_clause_set,
                                           branch_partial_assignment,
                                           False, use_max_heuristic)
            if branch_result is not False:
                return branch_result  # SAT

        return False  # UNSAT


# === OWN TESTING ===
# if __name__ == '__main__':
#     # print(simple_sat_solve([]))
#
#     def test_file(path, n=10, average=True):
#         print(f'###TESTING {path}###')
#         test_clause_set = load_dimacs(path)
#         # print(test_clause_set)
#         start = time.time()
#         dpll_output = dpll_sat_solve(test_clause_set, [], use_max_heuristic=True)
#         print(time.time() - start, dpll_output)
#         if dpll_output is not False:  # could be [] which is valid
#             if not check_sat_assignment(load_dimacs(path), dpll_output):
#                 print('OUTPUT INVALID')
#
#         if average:
#             print(' - Average time tests:')
#             total = 0
#             for _ in trange(n):
#                 test_clause_set = load_dimacs(path)
#                 start = time.time()
#                 dpll_sat_solve(test_clause_set, [], use_max_heuristic=True)
#                 total += time.time() - start
#
#             print(f'Averaged over {n} tests: {total/n}s')
#
#
#     # test_file('Sample SAT tests/W_2,3_ n=8 (SAT).txt')
#     test_file('Sample SAT tests/8queens (SAT).txt', average=True)
#     test_file('Sample SAT tests/hole6 (UNSAT).txt')
#     # test_file('Sample SAT tests/uf50-01.cnf', average=False)
#     # test_file('Sample SAT tests/uuf50-01.cnf', average=False)
#     test_file('Sample SAT tests/uf100-01.cnf', average=True)
#     # test_file('Sample SAT tests/uuf100-01.cnf', average=True)
#     test_file('Sample SAT tests/uf150-01.cnf', average=False)
#     # test_file('Sample SAT tests/uuf150-01.cnf', average=False)
#
#     # start = time.time()
#     # print(simple_sat_solve(test_clause_set, print_all=True), 'simple', time.time() - start)
#     # start = time.time()
#     # print(branching_sat_solve(test_clause_set, []), 'branching', time.time() - start)
#
#     # Practical Exercises Wk14 Q7.3:
#     practical_ex = [[1, 2, 3], [1, -2, -4], [2, -3, 4], [-1, 3, 4], [-1, 2, -4],
#                     [1, -2, -3], [-1, -2, 4], [-1, -3, -4]]
#     print(simple_sat_solve(practical_ex))
#     print(branching_sat_solve(practical_ex, []))
#     print(dpll_sat_solve(practical_ex, []))
