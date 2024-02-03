from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon


def cfg_to_wcnf(grammar: CFG):

    """Takes a context-free grammar and turns it to weak Chomsky Normal Form"""

    var_name = 0

    # removing productions with long bodies

    productions = set()
    variables = set(grammar.variables)

    for production in grammar.productions:
        if len(production.body) > 2:
            head = production.head
            item = production.body[0]

            var = Variable("V" + str(var_name))
            variables.add(var)
            var_name += 1

            productions.add(Production(head, [item, var]))

            for i in range(1, len(production.body) - 2):
                head = var
                item = production.body[i]

                var = Variable("V" + str(var_name))
                variables.add(var)
                var_name += 1

                productions.add(Production(head, [item, var]))

            item1 = production.body[len(production.body) - 2]
            item2 = production.body[len(production.body) - 1]
            productions.add(Production(var, [item1, item2]))

        else:
            productions.add(production)

    new_grammar = CFG(variables, grammar.terminals, grammar.start_symbol, productions)
    # print(new_grammar.to_text(), 'long bodies')

    new_grammar = new_grammar.eliminate_unit_productions()
    # print(new_grammar.to_text(), 'eliminate_unit_productions')
    new_grammar = new_grammar.remove_useless_symbols()
    # print(new_grammar.to_text(), 'remove_useless_symbols')

    # removing V -> t t and V -> V t productions

    productions = set()
    variables = set(new_grammar.variables)

    variable_from_terminal = dict()

    for terminal in set(new_grammar.terminals):
        variable_from_terminal[terminal] = ""

    for production in set(new_grammar.productions):
        if len(production.body) == 1:
            variable_from_terminal[production.body[0]] = production.head

    for production in set(new_grammar.productions):
        body = []
        if len(production.body) == 2:
            for item in production.body:
                if type(item) is Terminal:

                    if variable_from_terminal[item] == "":
                        var = Variable("V" + str(item.value))
                        variables.add(var)
                        productions.add(Production(var, [item]))
                        variable_from_terminal[item] = var
                    else:
                        var = variable_from_terminal[item]

                    body.append(var)
                else:
                    body.append(item)
            productions.add(Production(production.head, body))
        else:
            productions.add(production)

    answer = CFG(
        variables, new_grammar.terminals, new_grammar.start_symbol, productions
    )
    # print(answer.to_text(), 'removed t and V t bodies')

    return answer


def cfg_from_file(file_name):

    """reads a CFG from a file"""

    file = open(file_name, "r")
    grammar = CFG.from_text(file.read())
    file.close()

    return grammar
