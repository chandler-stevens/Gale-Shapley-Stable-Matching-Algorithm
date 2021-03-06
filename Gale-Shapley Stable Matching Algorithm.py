# Chandler Stevens
# CSC 3430: Algorithm Design and Analysis
# Python 3 solution for stable matching problem
#  implemented with the Gale-Shapley Stable Matching Algorithm O(n^2)

# Import functions from timeit module for performance testing
from timeit import timeit, repeat


# Purpose: Get a valid element name from the user
# Parameters: (string) message representing prompt to user
#             (list of strings) takenNames representing taken names
# Returns: (string) name representing valid name
def getValidName(message, takenNames):
    # Ask user until valid input given
    while True:
        # Prompt user for input
        name = input(message)
        # If user input is not empty and is not taken
        if len(name) > 0 and name not in takenNames:
            # Then, return the user input integer
            return name
        # Otherwise, notify user of out of invalid name
        else:
            print("INVALID: Please enter a valid name.")


# Purpose: Get a valid integer from the user
# Parameters: (string) message representing prompt to user
#             (integer) minNum representing minimum allowed number
#             (integer) maxNum representing maximum allowed number
# Returns: (integer) num representing valid integer
def getValidInteger(message, minNum, maxNum):
    # Ask user until valid input given
    while True:
        # Try to convert input to integer
        try:
            # Prompt user for input and convert to integer
            num = int(input(message))
            # If user input integer is in valid range
            if minNum <= num <= maxNum:
                # Then, return the user input integer
                return num
            # Otherwise, notify user of out of range input integer
            else:
                raise ValueError
        # Catch value error and notify user of non-numerical input
        except ValueError:
            print("INVALID: Please enter an integer\n" +
                  "from " + str(minNum) + " to " + str(maxNum) + ".")


# Purpose: Get set X and set Y and the preferences from the user
# Parameters: None
# Returns: (integer) n representing count of elements in each set
#          (map) setX representing elements and preferences of set X
#          (map) setY representing elements and preferences of set Y
def getPreferences():
    # Initialize maps for set  X and set Y
    # Key: (string) Name of element
    # Value: (list of strings) Names of preferred elements from other set
    setX = {}
    setY = {}
    # Map each map to letter key to allow for code reuse
    sets = {"X": setX, "Y": setY}

    # Ask user for integer value of n from 2 to 100
    n = getValidInteger("How many elements are in each set?\n\t", 2, 100)

    # Ask user for the name of each element for both sets
    for setLetter in sets:
        # Start notification with appropriate word
        if setLetter == "X":
            word = "First"
        else:
            word = "Now"
        # Notify user of which set currently needs element names
        print("\n" + word + ", provide the elements from set " +
              setLetter + ":\n")
        # Ask user for element name
        for i in range(1, n + 1):
            sets[setLetter][getValidName("What is the name of element #" +
                                         str(i) + " from set " + setLetter +
                                         "?\n\t",
                                         list(sets[setLetter].keys()))] = []

    # Ask user for the preferences of each element for both sets
    for setLetter in sets:
        # Start notification with appropriate word
        if setLetter == "X":
            word = "\nNext"
            # Set opposite set to map setY
            opposite = sets["Y"]
        else:
            word = "Lastly"
            # Set opposite set to map setX
            opposite = sets["X"]
        # Notify user of which set currently needs element preferences
        print("\n" + word + ", provide the the preferences for " +
              "the elements of set " + setLetter + ":")
        # Extract map for current set
        _set = sets[setLetter]
        # Ask the user for preferences for each element
        for element in _set:
            # Notify user of which element currently needs preferences
            print("\nNow for the preferences of " + element + ":\n")
            # Prepare list of un-prioritized element names from opposite set
            preferences = list(opposite.keys())
            # While there are still multiple preferences to prioritize
            while len(preferences) > 1:
                # Prompt user for next highest preference of current element
                print("Type the number of the next highest preference for " +
                      element + ":")
                # Display the remaining preferences to prioritize
                for i, y in enumerate(preferences, start=1):
                    print(y + " (" + str(i) + ")")
                # Remove user input from remaining un-prioritized list and
                #  append to list of respective list of element in map
                _set[element].append(preferences.pop(
                    getValidInteger("\t", 1, len(preferences)) - 1))
            # Remove sole remaining un-prioritized preference and
            #  append to list of respective list of element in map
            _set[element].append(preferences.pop())

    # Return n count, set X map, and set Y map
    return n, setX, setY


# Purpose: Determine a possible stable matching between preferences of set X
#           and preferences of set Y with both sets of equal count n
# Parameters: (integer) n representing count of elements in each set
#             (map) setX representing elements and preferences of set X
#             (map) setY representing elements and preferences of set Y
# Returns: yMatches (map) representing a possible stable matching
def galeShapleyAlgorithm(n, setX, setY):
    # Declare map to represent prioritized preferences of each element of set Y
    # Key: (string) Name of element y of set Y
    # Value: (map) Name and index of preference from set X of y
    # Note: Maps are almost guaranteed a time complexity of O(1) for lookups,
    #       which offers high optimization of performance at the expense of
    #       space complexity, especially with nested maps as done here
    yPreferences = {}
    # Populate yPreferences map
    # Iterate through each element y in set Y and keep track of current index
    for i, yTuple in enumerate(list(setY.items())):
        # Declare map to represent the prioritized preferences of y
        # Key: (string) Name of preference x from set X
        # Value: (integer) Index (priority level) of x
        priority = {}
        # Populate priority map
        # Iterate through each x in the preferences list of y
        for j, preference in enumerate(yTuple[1]):
            # Add name of x and index of x to priority map
            priority[preference] = j
        # Add name of y and prioritized preferences map of y to yPreferences map
        yPreferences[yTuple[0]] = priority

    # Free memory to reduce space complexity
    del setY, j, preference, priority

    # Declare map to represent the currently unmatched elements of set X
    # Key: (integer) Name of element x from set X
    # Value: (list of strings) Preferences from set Y of x
    xUnmatched = {}
    # Populate xUnmatched map
    for i, x in enumerate(setX):
        # Add preferences of x to xUnmatched map
        xUnmatched[x] = setX[x]

    # Free memory to reduce space complexity
    del setX

    # Declare map to represent current existing matches
    # Key: (string) Name of element of set Y
    # Value: (string) Name of element of set X
    yMatches = {}

    # Declare map to represent the currently matched elements of set X
    # Key: (integer) Name of element x from set X
    # Value: (list of strings) Preferences from set Y of x
    xMatched = {}

    # Initialize count of unmatched elements of set X to n
    xUnmatchedCount = n

    # While there are still unmatched elements of set X
    while xUnmatchedCount > 0:
        # Get the first unmatched element x of set X
        xTuple = list(xUnmatched.items())[0]
        # Extract the name of x
        x = xTuple[0]
        # Extract the list of preferences from set Y
        xPreferences = xTuple[1]

        # Initialize counter index to zero
        i = 0
        # While x is still unmatched and
        #  there are still untested preferences of x to check
        # Note: This single nested while loop is what makes this
        #       algorithm have a time complexity of O(n^2)
        while x in xUnmatched and i < n:
            # Extract the first remaining preference y
            y = xPreferences[i]
            # If y is not already matched with any other element of set X
            if y not in yMatches:
                # Then, match x with y
                # Set the current match of y as x
                yMatches[y] = x
                # Move x name from the xUnmatched map to the xMatched map
                xMatched[x] = xUnmatched.pop(x)
                # Decrement the count of unmatched elements of set X
                xUnmatchedCount -= 1
            # Otherwise, if y is already matched with a
            #  different element of set X
            else:
                # Then, check if y prefers x over the current match of y
                # Determine the current match of y
                yCurrentMatch = yMatches[y]
                # Extract the list of preferences of y from the yPreferences map
                yPreference = yPreferences[y]
                # If the priority level of x is higher than
                #  the priority level of the current match of y
                if yPreference[x] < yPreference[yCurrentMatch]:
                    # Move the current match of y from the xMatched map
                    #  to the xUnMatched map
                    xUnmatched[yCurrentMatch] = xMatched.pop(yCurrentMatch)
                    # Then, match x with y instead
                    # Set the current match of y as x
                    yMatches[y] = x
                    # Move x name from the xUnmatched map to the xMatched map
                    xMatched[x] = xUnmatched.pop(x)
                    # Note: Do not change xUnmatchedCount since the
                    #       net gain/loss is zero since one element
                    #       from x was matched while one other was unmatched.
                # Otherwise, if y does not prefer x over the current match of y
                else:
                    # Increment the counter index to check
                    #  the next remaining preference
                    i += 1

    # Return the final result of a possible stable matching
    #  between the preferences of set X and set Y
    return yMatches


# Purpose: Display the possible stable matches of a stable matching
# Parameters: (map) result representing a stable matching
#              Key: (string) Name of element y from set Y
#              Value: (string) Name of element x from set X
# Returns: yMatches (map) representing a possible stable matching
def displayResult(result):
    print("\n\nA possible stable matching between set X and set Y is:")
    # Display each match as "x matched with y"
    for y in result:
        print(str(result[y]) + " matched with " + str(y))


# Purpose: Measure execution time of Gale-Shapely Stable Matching Algorithm
# Parameters: (integer) n representing count of elements in each set
#             (map) setX representing elements and preferences of set X
#             (map) setY representing elements and preferences of set Y
#             (boolean) single representing whether to time a single execution
# Returns: time (float) Execution time in microseconds
def measurePerformance(n, setX, setY, single):
    if single:
        # Return the time of a single execution
        return timeit(lambda: galeShapleyAlgorithm(n, setX, setY),
                      number=1)
    else:
        # Return the shortest/fastest time of the three repetitions
        return min(
            # Perform three repetitions of one million iterations each
            repeat(lambda: galeShapleyAlgorithm(n, setX, setY)))


# Purpose: Main function to prepare two sets and match them
# Parameters: None
# Returns: Nothing
def main():
    # Get the elements of set X and set Y and the preferences
    n, setX, setY = getPreferences()
    # Get a possible stable matching between the preferences of set X and set Y
    stableMatching = galeShapleyAlgorithm(n, setX, setY)
    # Display the computed stable matching
    displayResult(stableMatching)

    # Ask user whether to proceed to execution time analysis
    if input("\nWould you also like to measure the performance? " +
             "(y/n)\n\t").lower() == "y":
        # Ask user whether to perform average or single measurement
        if input("\nDo you want to time a single execution or\n" +
                 "time the average of three million executions? " +
                 "(s/a)\n\t").lower() == "a":
            single = False
            word = "average"
        else:
            single = True
            word = "single execution"
        print("Measuring " + word + " performance ...")
        # Display execution time in microseconds rounded to 6 decimals
        print("\nThe stable matching was determined in about\n" +
              str(round(measurePerformance(n, setX, setY, single), 6)) +
              " microseconds.")
    # Do not immediately close program on user
    input("Press any key to exit ...")


# # RESULT OF BEST CASE: NO CONFLICTING TOP PREFERENCES
# displayResult(
#     galeShapleyAlgorithm(4,
#                          {"Ben": ["Rey", "Jyn", "Padme", "Leia"],
#                           "Cassian": ["Jyn", "Leia", "Rey", "Padme"],
#                           "Anakin": ["Padme", "Jyn", "Rey", "Leia"],
#                           "Han": ["Leia", "Jyn", "Padme", "Rey"]},
#                          {"Rey": ["Ben", "Anakin", "Han", "Cassian"],
#                           "Jyn": ["Cassian", "Han", "Anakin", "Ben"],
#                           "Padme": ["Anakin", "Han", "Cassian", "Ben"],
#                           "Leia": ["Han", "Cassian", "Ben", "Anakin"]}
#                          )
# )
#
# # TIMING OF BEST CASE: NO CONFLICTING TOP PREFERENCES
# print("The stable matching was determined in about\n" +
#       str(
#           round(
#               measurePerformance(4,
#                                  {"Ben": ["Rey", "Jyn", "Padme", "Leia"],
#                                   "Cassian": ["Jyn", "Leia", "Rey", "Padme"],
#                                   "Anakin": ["Padme", "Jyn", "Rey", "Leia"],
#                                   "Han": ["Leia", "Jyn", "Padme", "Rey"]},
#                                  {"Rey": ["Ben", "Anakin", "Han", "Cassian"],
#                                   "Jyn": ["Cassian", "Han", "Anakin", "Ben"],
#                                   "Padme": ["Anakin", "Han", "Cassian", "Ben"],
#                                   "Leia": ["Han", "Cassian", "Ben", "Anakin"]},
#                                  False
#                                  ),
#               6)
#       )
#       + " microseconds.")
#
# # RESULT OF WORST CASE: COMPLETELY CONFLICTING TOP PREFERENCES
# displayResult(
#     galeShapleyAlgorithm(4,
#                          {"Ben": ["Leia", "Padme", "Jyn", "Rey"],
#                           "Cassian": ["Leia", "Padme", "Jyn", "Rey"],
#                           "Anakin": ["Leia", "Padme", "Jyn", "Rey"],
#                           "Han": ["Leia", "Padme", "Jyn", "Rey"]},
#                          {"Rey": ["Han", "Anakin", "Cassian", "Ben"],
#                           "Jyn": ["Han", "Anakin", "Cassian", "Ben"],
#                           "Padme": ["Han", "Anakin", "Cassian", "Ben"],
#                           "Leia": ["Han", "Anakin", "Cassian", "Ben"]}
#                          )
# )
#
# # TIMING OF WORST CASE: COMPLETELY CONFLICTING TOP PREFERENCES
# print("The stable matching was determined in about\n" +
#       str(
#           round(
#               measurePerformance(4,
#                                  {"Ben": ["Leia", "Padme", "Jyn", "Rey"],
#                                   "Cassian": ["Leia", "Padme", "Jyn", "Rey"],
#                                   "Anakin": ["Leia", "Padme", "Jyn", "Rey"],
#                                   "Han": ["Leia", "Padme", "Jyn", "Rey"]},
#                                  {"Rey": ["Han", "Anakin", "Cassian", "Ben"],
#                                   "Jyn": ["Han", "Anakin", "Cassian", "Ben"],
#                                   "Padme": ["Han", "Anakin", "Cassian", "Ben"],
#                                   "Leia": ["Han", "Anakin", "Cassian", "Ben"]},
#                                  False
#                                  ),
#               6)
#       )
#       + " microseconds.")

main()
