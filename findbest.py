def find_best_computer2(computers, budget):
    # Calculate value for each computer (score-to-cost ratio)
    for computer in computers:
        computer['Value'] = computer['Score'] / computer['Cost'] if computer['Cost'] > 0 else float('inf')

    # Sort computers based on value in descending order
    sorted_computers = sorted(computers, key=lambda x: x['Value'], reverse=True)

    # Select computers that fit within the budget
    selected_computers = []
    current_best = None
    
    for computer in sorted_computers:
      
      if budget >= computer['Cost'] and computer['Score'] >= 50:
        if not current_best:
            current_best = computer
        elif computer['Score'] > current_best['Score']:
            current_best = computer
            selected_computers.append(computer)
        else:
            selected_computers.append(computer)
    selected_computer =sorted(selected_computers, key=lambda x: x['Score'], reverse=True)

        #still needs optimization in case device doesnt have GPU
      #else:
       # print(f"ComputerID: {computer['GamingID']} is not a good computer currently for your budget and we highly recommend you look for other devices")
            
    
    return selected_computer[0:3:1]
