import streamlit as st
import requests
import json

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

def bayes(a, b, ba):
	"""Uses Bayes' rule to compute P(A|B). Takes P(A), P(B), and P(B|A), in that order."""
	return round(100 * (ba * a) / b, 2)


def get_stats(state):
	"""Gets vaccination rate and test positivity rate for selected state."""
	result = requests.get(
		f"https://api.covidactnow.org/v2/state/{us_state_abbrev[state]}.json?apiKey=72c3e14e79124546baf9901630cf7a25").json()
	return result['metrics']['testPositivityRatio'], result['metrics']['vaccinationsCompletedRatio']


def main():
	st.title("I really shouldn't have had to make this.")
	st.text("""
		There are way too many headlines circulating right now that say something
		like "X% of people in Y region's COVID outbreak were vaccinated". When
		you think about it, that statistic (while making wonderful headlines)
		means absolutely nothing. What we actually care about, is the opposite:
		how likely is an individual to be infected given that they are vaccinated?

		This tool converts between what the headlines say and what we actually care about. 
		""")
	st.header("How to use this tool")
	ba = st.text_input("""1. Give us the number the article said (something along the lines of "X% of people in outbreak were vaccinated").\n""", 
		value="25.7%", 
		help="Enter a percentage 0-100")

	if len(ba) == 0:
		ba = "-1"
	if ba[-1] == "%": # strip the percent sign if it's there
		ba = ba[:-1]

	if ba.replace(".", "1").isdigit() and (0 <= float(ba) <= 100):
		state = st.selectbox("2. Select your state.", list(us_state_abbrev.keys()))
		calc = st.button("Calculate")
		if calc:
			st.markdown(f"#### If you're vaccinated, you have a {bayes(*get_stats(state), ba=float(ba) / 100)}% chance of getting COVID in {state}.")
		st.header("How does this work?")
		st.text("This.")
		st.latex(r"P(\text{infected} | \text{vaccinated}) = \frac{P(\text{infected}) \cdot P(\text{vaccinated} | \text{infected})}{P(\text{vaccinated})}")
		st.markdown("We pull probability of infection (test positivity ratio) and probability of vaccination (percent fully vaccinated) from [Covid ActNow](https://apidocs.covidactnow.org).")
		st.header("Are you a healthcare professional?")
		st.text("No. Please don't mistake this for medical advice.")
	else:
		st.markdown(":warning: **Enter a value 0-100**")


if __name__ == '__main__':
	main()