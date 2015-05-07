import glob
import datetime
import matplotlib.pyplot as plt
import numpy as np
#import re

__author__ = 'amaralian'
__email__ = 'my_email@something.com'

def find_student_records(directory: "pathlib object", extension = "txt") -> list:
    """
    Find all the student records in the specified directory. Specifying extension
    is optional; defaults to "txt"

    Returns an iterator.
    """

    paths = glob.iglob(directory + '/*.' + extension)
    return paths


def calculate_age(dob: "datetime object", today: "datetime object" = None) -> int:
    """Calculate the age of someone born on 'dob' on date 'today'
    (today if not specified)"""

    if today is None:
        today = datetime.datetime.today()

    correction = 0
    if today.month < dob.month:
        correction = 1
    elif today.month == dob.month and today.day < dob.day:
        correction = 1

    age = today.year - dob.year - correction

    return age


def clean_dob(dob: "string of form M/D/YY") -> datetime.datetime:
    """Reimplements date from string M/D/YY as datetime.datetime object"""

    month, day, year = dob.split('/')

    month = int(month)
    day = int(day)
    year = int(year)

    year += 1900
    if year < 1920:
        year += 100

    dob = datetime.datetime(year=year, month=month, day=day)

    return dob


def clean_height(height: "string of form n ft,m in") -> int:
    """Reimplements height from string nft,min as int """

    split_height = height.strip().split(',')
    feet = int(split_height[0].strip('ft'))
    inches = int(split_height[1].strip('in'))
    numeric_height = 12 * feet + inches

    return numeric_height


def clean_weight(weight: "string of form n lbs") -> float:
    """Reimplements weight from string of form n lbs as float"""

    numeric_weight = float( weight.strip("lbs") )

    return numeric_weight


def parse_student_record(path: "pathlib object",
                         separator: "string that separate key from value" = ":") -> dict:
    """Load a data file"""

    data = {}

    with open(path) as file:
        for line in file:
            # ignore comment lines (those that start with "#")
            if line.startswith('#'):
                continue

            # split the line
            parts = line.split(separator)

            # make sure the line has the correct number of parts
            if len(parts) != 2:
                continue

            # clean up the parts (strip whitespace) and store them
            key, value = parts
            key = key.strip()
            value = value.strip()

            data[key] = value

    data['Date of Birth'] = clean_dob(data['Date of Birth'])
    data['Weight'] = clean_weight(data['Weight'])
    data['Height'] = clean_height(data['Height'])

    return data


def half_frame_mpl(sub: "axis object", font_size: "int",
                   x_string: "x-axis label",
                   y_string: "y-axis label") -> None:
    """Format graph frame, tick marks, and axis' labels"""

    sub.yaxis.set_ticks_position('left')
    sub.xaxis.set_ticks_position('bottom')
    sub.tick_params(axis = 'both', which = 'major', length = 7,
                    width = 2, direction = 'out', pad = 10,
                    labelsize = font_size)
    sub.tick_params(axis = 'both', which = 'minor', length = 5,
                    width = 2, direction = 'out',
                    labelsize = 0.6 * font_size)
    for axis in ['bottom','left']:
        sub.spines[axis].set_linewidth(2)
        sub.spines[axis].set_position(("axes", -0.02))
    for axis in ['top','right']:
        sub.spines[axis].set_visible(False)

    # Format axes
    sub.set_xlabel(x_string, fontsize = 1.6 * font_size)
    sub.set_ylabel(y_string, fontsize = 1.6 * font_size)



##### Our code
personnel_data = []
for i, file in enumerate( find_student_records("../Bootcamp/Data/Roster") ):
    personnel_data.append( parse_student_record(file) )
    #print(i, personnel_data[0]["Height"])

# Extract all heights into a numpy array and plot a histogram
my_heights = []
for person in personnel_data:
    my_heights.append(person["Height"])

all_heights = np.array(my_heights)
print(all_heights.shape)

fig = plt.figure( figsize = (12, 4.5) )
sub1 = fig.add_subplot(1,2,1)
sub2 = fig.add_subplot(1,2,2)

# Set baseline font size
my_font_size = 12
half_frame_mpl(sub1, my_font_size, "height [in]", "Probability density")
half_frame_mpl(sub2, my_font_size, "weight [lbs]", "Probability density")

# Add and format data sets
sub1.hist(all_heights, 20, normed = 1, rwidth = 0.75, color = "g",
          alpha = 0.5, histtype = "bar", label = "Heights",
          cumulative = False)
#sub1.hist(x, z, "bo-", label = "Linear")


# Format legend
sub1.legend(loc = "best", frameon = False,
            markerscale = 1.8, fontsize = my_font_size)

plt.tight_layout()
plt.show()