def find_rule(rule):
    file = open("MagicCompRules.txt", encoding="utf8")
    if rule.lower() == "random":
        lines = file.read().splitlines()
        random_rule = ""
        while not re.match(r"[0-9][0-9][0-9][.][0-9]+[a-z]+", random_rule):
            random_rule = random.choice(lines)
        return random_rule
    else:
        line = str(file.readline())
        count = 1
        while line:
            if line.startswith(rule):
                return line
            line = file.readline()
            count += 1
    return "Rule " + rule + " could not be found"
