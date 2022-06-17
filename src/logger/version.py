if __name__ == "__main__":
    version = 0
    with open("version", "r") as file:
        version = int(file.read()) + 1
    with open("version", "w") as file:
        file.write(str(version))
