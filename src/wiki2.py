import requests
import mwparserfromhell

# Construction custom user-agent for query
custom_agent = {
    'User-Agent': 'some-agent',
    'From': 'name@domain.com' 
}

# Construct the parameters of the API query
parameters = {
    'action': 'parse',
    'prop': 'wikitext',
    'format': 'json',
    'page': 'Abyssal_whip'
}

# Call the API using the custom user-agent and parameters
result = requests.get('https://oldschool.runescape.wiki/api.php', 
                        headers=custom_agent, 
                        params=parameters).json()

# Grab the actual wikitext portion of the result
data = result["parse"]["wikitext"]["*"].encode("utf-8")
print(data)

# Use mwparserfromhell to read in the wikitext
wikicode = mwparserfromhell.parse(data)

templates = wikicode.filter_templates()
for template in templates:
    template_name = template.name.strip()
    print("Template name:", template_name)
    #if "infobox item" in template_name.lower():
    for param in template.params:
        param_name = param.name.strip()
        param_value = param.value.strip()
        print(f"Parameter name: {param_name}, Parameter value: {param_value}")
    print("\n" + "-"*40 + "\n")