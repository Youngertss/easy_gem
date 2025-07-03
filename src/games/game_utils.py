import random

def find_indices(lst, value):
    return [i for i, x in enumerate(lst) if x == value]

def wheelIncome(fortune_wheel_data):
    labels = fortune_wheel_data['labels']
    weights = fortune_wheel_data["weights"]
    sector_degree = 360/len(labels)
    
    prize = random.choices(labels, weights=weights, k=1)[0]  #random value based on weights
    indices = find_indices(labels, prize) #indecies with prize
    index = random.choices(indices)[0] #radnom index with prize

    degree_start = sector_degree * index
    degree_end = sector_degree * (index+1)
    
    degree = round(random.uniform(degree_start+0.1, degree_end-0.1), 2) #random degree the is in certain sector
    print((degree + 360*4 + (3*sector_degree+15)) % 360)
    return {"income":prize, "degree": degree + 360*4 + (3*sector_degree+15)} 
#(3*sector_degree+15) bcs the wheel starts from -15 and -(3 sectors) degree at the page.


# fortune_wheel_data = {
#     'cost': 15, 
#     'labels': [10, 0, 777, 5, 1, 20, 50, 2, 15, 1, 100, 5], 
#     "weights": [0.2, 0.1, 0.02, 0.25, 0.2, 0.4, 0.15, 0.2, 0.8, 0.2, 0.1, 0.25],
#     'labels_sorted': [0, 1, 1, 2, 5, 5, 10, 15, 20, 50, 100, 999]
# }
# res = wheelIncome(fortune_wheel_data)
# print(res)

## average income test
# sum = 0
# for i in range(100):
#     res = wheelIncome(fortune_wheel_data)
#     sum += res
    
# print(sum/100)