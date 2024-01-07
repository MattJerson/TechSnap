from findbest import  find_best_computer2
import json
f = open('json/GamingPCDataset.json')
d = open('json/ProfessionalPCDataset.json')
l = open('json/GamingLaptopDataset.json')
s = open('json/ProfessionalLaptopID.json')
dataset = json.load(f)
profdataset =json.load(d)
laptop =json.load(l)
proflapset =json.load(s)
def knapsack(computers, budget):
    n = len(computers)
    
    # Initialize a table to store results
    table = [[0] * (budget + 1) for _ in range(n + 1)]

    # Build the table using dynamic programming
    for i in range(1, n + 1):
        for w in range(budget + 1):
            cost = int(computers[i - 1]["Cost"])  # Convert to integer
            score = int(computers[i - 1]["Score"])  # Convert to integer

            if cost > w:
                table[i][w] = table[i - 1][w]
            else:
                table[i][w] = max(table[i - 1][w], table[i - 1][w - cost] + score)

    # Trace back to find selected computers
    selected_computers = []
    i, j = n, budget
    while i > 0 and j > 0:
        if table[i][j] != table[i - 1][j]:
            selected_computers.append(computers[i - 1])
            j -= int(computers[i - 1]["Cost"])  # Convert to integer
        i -= 1

    return selected_computers

def run_function(category,subcategory,budget):
    if(category == 'Gaming'.lower()):
        if(subcategory == 'PC'.lower()):
            selected_computers = knapsack(dataset[0], budget)
            best_computer = find_best_computer2(dataset[0], budget)
            #return [selected_computers,best_computer]
            return [selected_computers, best_computer]
        else:
            selected_computers = knapsack(laptop[0], budget) 
            best_computer = find_best_computer2(laptop[0], budget)
            return [selected_computers, best_computer]
    else:
        if(subcategory == 'PC'.lower()):
            selected_computers = knapsack(profdataset[0], budget)
            best_computer = find_best_computer2(profdataset[0], budget)
            #return [selected_computers,best_computer]
            return [selected_computers, best_computer]
        else:
            selected_computers = knapsack(proflapset[0], budget)
            best_computer = find_best_computer2(proflapset[0], budget)   
            return [selected_computers, best_computer]

def return_string(selected, best):
    stringtable = []
    for computer in selected:
        stringtable.append(f"Best Budget deals when buying more than one Computer -> Computer ID: {computer['ID']}, Cost: ${computer['Cost']}, Bottleneck score: {round(100-computer['Score'],2)}")
    for computer in best:
        stringtable.append(f"Best Computer to buy with your current budget -> Computer ID: {computer['ID']}, Cost: ${computer['Cost']}, Bottleneck score: {round(100-computer['Score'],2)}")
    return stringtable





   

