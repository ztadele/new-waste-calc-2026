from drafter import *
from dataclasses import dataclass
from bakery import assert_equal

set_website_title("Waste Calculator")
set_site_information(
    author="Zoe Tadele",
    description="Waste calculator that takes inb waste values for an area and returns a grade for that area.",
    sources="Thanks to the Drafter docs and my LLMs.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/ztadele/new-waste-calc-2026", 
           "https://docs.google.com/document/d/11vAyJCyHmUyOwMJvHo3WGte7SLyJFd03FnJKTQXB5ms/edit?usp=sharing",
           "https://docs.google.com/document/d/1CNqmLDPh3cgLxsoYa_QDdR5wQlm9tF97VsUNM5Dj8GU/edit?usp=sharing",
          "https://docs.google.com/document/d/1DzrbelletEesy8-ZcCAqgYb1OftCqaC52mWdr1g0kiM/edit?usp=sharing"]
)
hide_debug_information()
set_website_framed(False)



@dataclass
class Waste:
    """Store information about one waste entry."""
    area: str
    waste_type: str
    waste_amount: int


@dataclass
class WasteCategory:
    """Store information about a waste category and its disposal method."""
    waste_category_name: str
    is_recyclable: bool
    disposable_method: str


@dataclass
class State:
    """Store the information used throughout the waste calculator."""
    area: str
    waste_list: list[Waste]
    waste_type: str
    waste_amount: int
    total_waste: int
    grade: str
    waste_categories: list[WasteCategory]


def create_initial_state():
    """Create the initial state with empty waste information."""
    return State("", [], "", 0, 0, "", [
        WasteCategory("Plastic", True, "Place in the recycling bin."),
        WasteCategory("Paper", True, "Place in the recycling bin."),
        WasteCategory("Glass", True, "Place in the recycling bin."),
        WasteCategory("Metal", True, "Place in the recycling bin."),
        WasteCategory("Other", False, "Dispose of according to local guidelines.")
    ])


def can_recycle(waste_type: str) -> bool:
    """Check whether a waste type is recyclable.

    Args:
        waste_type: The name of the waste category.

    Returns:
        True if the waste can be recycled, otherwise False.
    """
    waste_type = waste_type.lower()
    if waste_type == "plastic":
        return True
    elif waste_type == "glass":
        return True
    elif waste_type == "metal":
        return True
    elif waste_type == "paper":
        return True
    else:
        return False


def waste_present(waste_amount: int) -> str:
    """Describe the amount of waste recorded.

    Args:
        waste_amount: The total amount of waste in pounds.

    Returns:
        A message describing the waste amount.
    """
    if waste_amount == 0:
        return "No waste found, try again!"
    elif waste_amount > 50:
        return "high waste amount (greater than 50 lbs)"
    else:
        return "low waste count (less than 50 lbs)"


def save_waste_entry(state: State) -> State:
    """Add a new waste entry and update the total waste.

    Args:
        state: The current calculator state.

    Returns:
        The updated calculator state.
    """
    new_waste = Waste(
        state.area,
        state.waste_type,
        state.waste_amount
    )
    state.waste_list.append(new_waste)
    state.total_waste = 0
    for item in state.waste_list:
        state.total_waste += item.waste_amount
    return state


@route
def index(state: State) -> Page:
    """Display the welcome page and link to the input page."""
    return Page(state, [
        Header("Welcome to the Waste Calculator!"),
        Text("Hi! This is the home page for our waste calculator website."),
        Text("Enter your waste information."),
        Button("Go to Inputs Page", "add_waste")
    ])


@route
def add_waste(state: State) -> Page:
    """Display the input boxes for the user's area and waste amount."""
    return Page(state, [
        Header("Add Waste Page"),
        Text("Enter your waste information:"),
        Text("Enter Area:"),
        TextBox("area", state.area),
        Text("Enter Waste Amount (lbs):"),
        TextBox("waste_amount", state.waste_amount, "number"),
        Button("Submit Waste", "waste_categories"),
        Button("Back to Start", "index")
    ])


@route
def waste_categories(state: State, area: str, waste_amount: int) -> Page:
    """Save the user's information and display available waste categories.

    Args:
        area: The area where the waste was produced.
        waste_amount: The amount of waste in pounds.
    """
    state.area = area
    state.waste_amount = waste_amount

    category_text = []
    for category in state.waste_categories:
        category_text.append(
            Text(category.waste_category_name + ": " + category.disposable_method)
        )

    return Page(state, [
        Header("Waste Categories Page"),
        Text("Please select your waste type:"),
        *category_text,
        SelectBox("waste_type", ["Plastic", "Paper", "Glass", "Metal", "Other"]),
        Button("Submit Waste", "view_waste"),
        Button("Back to Add Waste", "add_waste")
    ])


@route
def view_waste(state: State, waste_type: str) -> Page:
    """Save the selected waste type and display the total waste amount.

    Args:
        waste_type: The waste category selected by the user.
    """
    state.waste_type = waste_type

    if state.area.strip() == "" or state.waste_amount <= 0:
        return Page(state, [
            Header("Invalid Waste Information"),
            Text("Please enter a valid area and a waste amount greater than zero."),
            Button("Back to Add Waste", "add_waste")
        ])

    state = save_waste_entry(state)

    return Page(state, [
        Header("Your Total Waste"),
        Text("Here is your waste calculation:"),
        Text(str(state.total_waste)),
        Text("Amount of total waste recorded (in pounds)."),
        Button("View Waste Grade", "return_grade")
    ])


@route
def return_grade(state: State) -> Page:
    """Calculate and save a letter grade based on total waste."""
    if state.total_waste <= 10:
        state.grade = "A"
    elif state.total_waste <= 25:
        state.grade = "B"
    elif state.total_waste <= 50:
        state.grade = "C"
    else:
        state.grade = "D"

    return Page(state, [
        Header("Waste Grade Calculation"),
        Text("Your waste grade has been calculated!"),
        Text("Your grade: " + state.grade),
        Button("Continue to Grade", "view_grade")
    ])


@route
def view_grade(state: State) -> Page:
    """Display the user's waste grade and feedback."""
    if state.grade == "A":
        feedback = "Excellent! You have a low amount of waste."
    elif state.grade == "B":
        feedback = "Good job! Your waste amount is pretty low."
    elif state.grade == "C":
        feedback = "Your waste amount is moderate. Consider recycling more or take a look at the advice on the next page."
    else:
        feedback = "Your waste amount is high. Try reducing and recycling waste and take a look at the advice on the next page."

    return Page(state, [
        Header("Your Waste Grade"),
        Text("Your final waste grade is:"),
        Text(state.grade),
        Text(feedback),
        Button("View Waste Advice", "view_advice")
    ])


@route
def view_advice(state: State) -> Page:
    """Display waste reduction advice based on the user's grade."""
    if state.grade == "A":
        advice = "Keep up the great work! Continue recycling and reducing waste."
    elif state.grade == "B":
        advice = "Try reusing containers and recycling paper, plastic, and metal."
    elif state.grade == "C":
        advice = "Consider composting food scraps and reducing single-use plastics."
    else:
        advice = "Start separating recyclable materials and look for ways to reuse items online."

    return Page(state, [
        Header("Waste Reduction Advice"),
        Text("Here is your personalized waste advice:"),
        Text(advice),
        Text("Recyclable: " + str(can_recycle(state.waste_type))),
        Text(waste_present(state.total_waste)),
        Button("Restart Calculator", "restart_calc")
    ])


@route
def restart_calc(state: State) -> Page:
    """Reset the user's waste information and display a confirmation page."""
    state.area = ""
    state.waste_list = []
    state.waste_type = ""
    state.waste_amount = 0
    state.total_waste = 0
    state.grade = ""

    return Page(state, [
        Header("Calculator Restarted"),
        Text("Your calculator has been reset!"),
        Text("You can now enter new waste information."),
        Button("Return to Start", "index")
    ])

# ---------------------------------------------------------------------------
# Unit tests (bakery). Test values are built inside helper functions so the
# file has no global variables.
# ---------------------------------------------------------------------------

def make_state(area: str = "", waste_amount: int = 0, waste_type: str = "",
               total_waste: int = 0, grade: str = "") -> State:
    """Build a fresh State with the given fields filled in for a test."""
    state = create_initial_state()
    state.area = area
    state.waste_amount = waste_amount
    state.waste_type = waste_type
    state.total_waste = total_waste
    state.grade = grade
    return state


def make_state_with_two_entries() -> State:
    """Build a State that has saved two waste entries (10 lbs and 5 lbs)."""
    state = make_state("Kitchen", 10, "Plastic")
    save_waste_entry(state)
    state.area = "Bedroom"
    state.waste_type = "Paper"
    state.waste_amount = 5
    return save_waste_entry(state)


# --- create_initial_state ---
assert_equal(create_initial_state().area, "")
assert_equal(create_initial_state().waste_list, [])
assert_equal(create_initial_state().waste_type, "")
assert_equal(create_initial_state().waste_amount, 0)
assert_equal(create_initial_state().total_waste, 0)
assert_equal(create_initial_state().grade, "")
assert_equal(len(create_initial_state().waste_categories), 5)
assert_equal(create_initial_state().waste_categories[0].waste_category_name,
             "Plastic")
assert_equal(create_initial_state().waste_categories[4].is_recyclable, False)

# --- can_recycle ---
assert_equal(can_recycle("plastic"), True)
assert_equal(can_recycle("Paper"), True)      # capitalization is ignored
assert_equal(can_recycle("GLASS"), True)
assert_equal(can_recycle("metal"), True)
assert_equal(can_recycle("other"), False)
assert_equal(can_recycle("banana peel"), False)

# --- waste_present ---
assert_equal(waste_present(0), "No waste found, try again!")
assert_equal(waste_present(1), "low waste count (less than 50 lbs)")
assert_equal(waste_present(50), "low waste count (less than 50 lbs)")
assert_equal(waste_present(51), "high waste amount (greater than 50 lbs)")
assert_equal(waste_present(200), "high waste amount (greater than 50 lbs)")

# --- save_waste_entry ---
assert_equal(make_state_with_two_entries().total_waste, 15)
assert_equal(len(make_state_with_two_entries().waste_list), 2)
assert_equal(make_state_with_two_entries().waste_list[0],
             Waste("Kitchen", "Plastic", 10))
assert_equal(make_state_with_two_entries().waste_list[1],
             Waste("Bedroom", "Paper", 5))

# --- index route ---
assert_equal(index(make_state()).state, make_state())
assert_equal(len(index(make_state()).content), 4)

# --- add_waste route ---
assert_equal(add_waste(make_state("Kitchen", 5)).state.area, "Kitchen")
assert_equal(len(add_waste(make_state()).content), 8)

# --- waste_categories route (saves area and amount) ---
assert_equal(waste_categories(make_state(), "Kitchen", 15).state.area,
             "Kitchen")
assert_equal(waste_categories(make_state(), "Kitchen", 15).state.waste_amount,
             15)
assert_equal(len(waste_categories(make_state(), "Kitchen", 15).content), 10)

# --- view_waste route (valid input) ---
assert_equal(view_waste(make_state("Kitchen", 15), "Plastic").state.waste_type,
             "Plastic")
assert_equal(view_waste(make_state("Kitchen", 15), "Plastic").state.total_waste,
             15)
assert_equal(len(view_waste(make_state("Kitchen", 15),
                            "Plastic").state.waste_list), 1)
assert_equal(len(view_waste(make_state("Kitchen", 15), "Plastic").content), 5)

# --- view_waste route (invalid input: blank area, then zero amount) ---
assert_equal(len(view_waste(make_state("", 15), "Plastic").content), 3)
assert_equal(view_waste(make_state("", 15), "Plastic").state.waste_list, [])
assert_equal(len(view_waste(make_state("Kitchen", 0), "Plastic").content), 3)
assert_equal(view_waste(make_state("Kitchen", 0),
                        "Plastic").state.total_waste, 0)

# --- return_grade route (every boundary) ---
assert_equal(return_grade(make_state(total_waste=5)).state.grade, "A")
assert_equal(return_grade(make_state(total_waste=10)).state.grade, "A")
assert_equal(return_grade(make_state(total_waste=11)).state.grade, "B")
assert_equal(return_grade(make_state(total_waste=25)).state.grade, "B")
assert_equal(return_grade(make_state(total_waste=26)).state.grade, "C")
assert_equal(return_grade(make_state(total_waste=50)).state.grade, "C")
assert_equal(return_grade(make_state(total_waste=51)).state.grade, "D")
assert_equal(len(return_grade(make_state(total_waste=5)).content), 4)

# --- view_grade route ---
assert_equal(view_grade(make_state(grade="A")).state.grade, "A")
assert_equal(view_grade(make_state(grade="D")).state.grade, "D")
assert_equal(len(view_grade(make_state(grade="B")).content), 5)

# --- view_advice route ---
assert_equal(view_advice(make_state(grade="A", waste_type="Glass",
                                    total_waste=5)).state.grade, "A")
assert_equal(view_advice(make_state(grade="B", waste_type="Plastic",
                                    total_waste=20)).state.total_waste, 20)
assert_equal(len(view_advice(make_state(grade="D", waste_type="Other",
                                        total_waste=60)).content), 6)

# --- restart_calc route (every field is reset) ---
assert_equal(restart_calc(make_state_with_two_entries()).state.waste_list, [])
assert_equal(restart_calc(make_state_with_two_entries()).state.total_waste, 0)
assert_equal(restart_calc(make_state("Kitchen", 20, "Plastic", 20, "B")
                          ).state.area, "")
assert_equal(restart_calc(make_state("Kitchen", 20, "Plastic", 20, "B")
                          ).state.waste_type, "")
assert_equal(restart_calc(make_state("Kitchen", 20, "Plastic", 20, "B")
                          ).state.waste_amount, 0)
assert_equal(restart_calc(make_state("Kitchen", 20, "Plastic", 20, "B")
                          ).state.grade, "")
assert_equal(len(restart_calc(make_state()).content), 4)


if __name__ == "__main__":
    start_server(create_initial_state())
