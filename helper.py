from utils import none_inference, is_consistent, is_assignment_complete, get_unassigned_variable, generate_CSP, generate_assignment, get_domain
import copy


def recursion_helper(assignment, CSP, solutions, multipleSolutions = False, inference_function = none_inference, is_consistent_function = is_consistent, get_unassigned_variable_function = get_unassigned_variable, get_domain_function = get_domain):
    if is_assignment_complete(assignment):
        if multipleSolutions:
            solutions.append(copy.deepcopy(assignment))
            return False

        solutions.append(assignment)
        return True

    variable = get_unassigned_variable_function(assignment, CSP)
    domain = get_domain_function(variable, CSP)

    for value in domain:
        if is_consistent_function(value, variable, assignment, CSP):
            # add the value to the assignment
            assignment.get(variable).append(value)

            inference_state, new_CSP = inference_function(CSP, variable, assignment)

            if inference_state: # the inference is successful
                backtrack_state = recursion_helper(assignment, new_CSP, solutions, multipleSolutions, inference_function, is_consistent_function)

                if backtrack_state and not multipleSolutions:
                    return True

            # the inference fails (a domain became empty)
            assignment.get(variable).remove(value)

    return False

