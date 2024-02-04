#Part 1 - take a list an multiply all list items together using a loop
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
result = 1
for num in part1:
    result *= num
print('Part 1 Answer: ',result)

#Part 2 - take a list and add all list items together
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
result2 = 0
for num in part2:
    result2 += num
print('Part 2 Answer: ',result2)

#Part 3 - add only the even numbers in this list
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 
result3 = 0
for num in part3:
    if(num % 2 == 0):
        result3+= num
print('Part 3 Answer: ',result3)
