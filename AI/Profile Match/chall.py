import pickle

FLAG = "d4rk{pr0f1le_m4tched_ez!!}"

with open("model.pkl", "rb") as f:
    model = pickle.load(f)


print("================================")
print("        PROFILE MATCH")
print("================================")
print()
print("Find the profile that produces")
print("a score of 100%. and you will be allowed to copy the flag.")
print()
print("Enter:")
print("The following parameters correctly for the admin account and trick the model into thinking you are the administrator.")
print()


try:
    

    age = int(input("> age : "))
    height = int(input("> height : "))
    weight = int(input("> weight : "))
    month = int(input("> month : "))
    year = int(input("> year : "))

    profile = [[
        age,
        height,
        weight,
        month,
        year
    ]]

    score = float(model.predict(profile)[0])

    # Clamp tiny ML prediction errors
    score = max(0.0, min(1.0, score))

    print()
    print(f"Score: {score * 100:.6f}%")

    if score >= 0.9999:
        print()
        print("ABSOLUTE 100% MATCH <=> ACCESS GRANTED")
        print("TAKE THE FLAG AS YOU LEAVE")
        print("==============================")
        print(FLAG)
        print("==============================")
    else:
        print("ACCESS DENIED")

except Exception:
    print("Invalid input.")