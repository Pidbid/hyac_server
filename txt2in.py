import re


def generate_requirements_in(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            package_name = re.split(r"[=<>#]", line)[0].strip()
            if package_name:
                outfile.write(package_name + "\n")


generate_requirements_in("requirements.txt", "requirements.in")
