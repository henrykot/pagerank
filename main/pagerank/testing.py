import random
testing = dict()
testing = {
    "1":0.1,
    "2":0.4,
    "3":0.3,
    "4":0.2
    }

# N = len(testing)
# page = "1"
# damping_factor = 0.8

# probability_distribution = {}
# for i in testing:
#     probability_distribution[i]=0

# direct_links = testing["1"]
# for j in direct_links:
#     probability_distribution[j]=damping_factor * 1 / N

# print (probability_distribution)

# for k in testing:
#    print (testing[k])


# for i in range (100):
            
#     chance = [testing[x] for x in testing]
#     previous_page = random.choices(list(testing.keys()), weights = chance, k = 1)
#     print (previous_page)

# testing["1"]+=1
# print (testing)

second_test = dict()
for i in testing:
    second_test [i] = 0

second_test ["10"] = ["ty","no","yes"]
value = "no"
if (value in second_test["10"]):
    print (second_test)