from fractions import Fraction
from decimal import Decimal

# Depending on user
x = 0.78
xDash = 0.22
red = [0.8, 0.05, 0.8, 0.05, 0.05, 0.8]
green = [0.2, 0.95, 0.2, 0.95, 0.95, 0.2]


# No change from here
start = ['1/3', '0', '1/3', '0', '0', '1/3']
states = [0, 1, 2, 3, 4, 5]

def normalize(fracs):
    sums = 0
    for item in fracs:
        sums += Fraction(str(item))
    print("Sum: ", sums)
    print("Sum: ", float(sums))
    for i in range(5):
        fracs[i] = Fraction(str(fracs[i]))/Fraction(str(sums))
        # print("Here: ", fracs[i])
    # print(fracs)
    return fracs

def multiply(a, b, c):
    # print(Fraction(str(a)))
    # print(Fraction(str(b)))
    # print(Fraction(str(c)))
    # print(Fraction(str(a))*Fraction(str(b))*Fraction(str(c)))
    return Fraction(str(a))*Fraction(str(b))*Fraction(str(c))

# print (multiply(start[4], xDash, red[4]))


# Right and Green
right = x
left = xDash
one = [0, 0, 0, 0, 0, 0]

for i in states:
    # print(i)
    if(i - 1 < 0):
        one[i] += multiply(start[i], left, green[i])
        one[i + 1] += multiply(start[i], right, green[i + 1])
    elif(i + 1 > 5):
        one[i - 1] += multiply(start[i], left, green[i - 1])
        one[i] += multiply(start[i], right, green[i])
    else:
        one[i - 1] += multiply(start[i], left, green[i - 1])
        one[i + 1] += multiply(start[i], right, green[i + 1])
    # print(one[3])
print(one)
print(normalize(one))
for i in range(6):
    print(float(one[i]), end=' ')
print()
print()
print()



# Left and Red
left = x
right = xDash
two = [0, 0, 0, 0, 0, 0]

for i in states:
    # print(i)
    if(i - 1 < 0):
        two[i] += multiply(one[i], left, red[i])
        two[i + 1] += multiply(one[i], right, red[i + 1])
    elif(i + 1 > 5):
        two[i - 1] += multiply(one[i], left, red[i - 1])
        two[i] += multiply(one[i], right, red[i])
    else:
        two[i - 1] += multiply(one[i], left, red[i - 1])
        two[i + 1] += multiply(one[i], right, red[i + 1])

print(two)
print(normalize(two))
for i in range(6):
    print(float(two[i]), end=' ')
print()
print()
print()


# Left And Green
left = x
right = xDash
three = [0, 0, 0, 0, 0, 0]

for i in states:
    # print(i)
    if(i - 1 < 0):
        three[i] += multiply(two[i], left, green[i])
        three[i + 1] += multiply(two[i], right, green[i + 1])
    elif(i + 1 > 5):
        three[i - 1] += multiply(two[i], left, green[i - 1])
        three[i] += multiply(two[i], right, green[i])
    else:
        three[i - 1] += multiply(two[i], left, green[i - 1])
        three[i + 1] += multiply(two[i], right, green[i + 1])

print(three)
print(normalize(three))
for i in range(6):
    print(float(three[i]), end=' ')
print()
print()
print()
