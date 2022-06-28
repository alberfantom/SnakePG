collection = {
    "something": {
        "one": 1,
        "two": 2,
        "three": 3
    },

    "five": 5,
    "six": 6
}

def draw(collection=None) -> None:
    for value in collection.values():
        if isinstance(value, dict):
            draw(collection=value)

        else:
            print(f"drawing an {value}")

draw(collection=collection)