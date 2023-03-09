input_file = open('input.txt')

num_targets = int(input_file.readline())

targets = [int(n) for n in input_file.readline().split(" ")]

prev_used = {1}
steps = []
counter = 0

for i in range(num_targets):
    cur_int = targets[i]
    while(True):
        if (cur_int in prev_used):
            break
        steps.append((str(max(prev_used)), 1))
        prev_used.add(max(prev_used)+1)
        
print(len(steps))
for i in steps:
    print(i[0],i[1])

