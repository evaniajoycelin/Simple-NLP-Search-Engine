from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.chunk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.probability import FreqDist

user_input = 0

dictionary_skin = {
    'Normal Skin':["Not too dry and not too oily, you have a radiant complexion, barely visible and fine pores.","You have velvety, soft and smooth texture, no blemishes, and not prone to sensitivity."],
    'Oily Skin':["Skin type with heightened sebum production, prone to comedones, blackheads, whiteheads and varying forms of acne.","You may have enlarged pores, dull or glossy shiny skin, thick complexion, pimples, or other blemishes."],
    'Combination Skin':["Your skin can be dry or normal in some areas and oily in others, such as the T-zone ( nose, forehead, and chin ) and the cheeks.", "You have pores that look larger than normal, shiny T-Zone, blackheads, normal to dry cheeks.","It may need different care in different areas"],
    'Dry Skin':["You may have almost invisible pores (small pores), dull or rough complexion, red patches, less elastic, and more visible lines.","Your skin can crack, peel, or become itchy, irritated, or inflamed because of dryness.","It can also become rough and scaly."],
    'Sensitive Skin':["Sensitive skin has subjective symptoms such as stinging, itching, burning, or another visible skin changes.","Some products can cause irritation, such as rashes, redness, dryness, scaling, peeling, bumps, hives."]
}

def validate_skin_input(input):

    if (any(char.isdigit() for char in input)):
        print("Input must be alphabet!")
        return False
    elif len(input) == 0:
        print("Can not empty!")
        return False
    elif(len(input.split())<2):
        print("Input must be more than 1 words!")
        return False

    return True

def validate_tips_input(input):
    if (any(char.isdigit() for char in input)):
        print("Input must be alphabet!")
        return False
    elif len(input) == 0:
        print("Can not empty!")
        return False
    elif(len(input.split())<3):
        print("Input must be more than 2 words!")
        return False

    return True

def skin_type():
    valid_input = False
    while not valid_input:
        my_skin = input("Your Skin Condition: ")
        valid_input = validate_skin_input(my_skin)

    #Remove stopwords
    english_stopwords = set(stopwords.words("english"))
    my_skin = my_skin.lower().split()
    my_skin = [word for word in my_skin if word not in english_stopwords]

    # Apply Stemming, I use Snowball Stemmer since it more accurate
    snow = SnowballStemmer("english")
    my_skin = [snow.stem(word) for word in my_skin]

    # Lemmatize
    lematizer = WordNetLemmatizer()
    my_skin = [lematizer.lemmatize(word) for word in my_skin]


    #Search the values of our dictionary
    found_type_desc = []
    found_type = []

    for word in my_skin:
        for type, type_desc in dictionary_skin.items():
            for desc in type_desc:
                if word in desc.lower() and desc not in found_type_desc:
                    found_type_desc.append(desc)
                    found_type.append(type)

    count_list = []
    type_list = []
    freq_dist = FreqDist(found_type)
    for fd, count in freq_dist.most_common():
        count_list.append(count)
        type_list.append(fd)

    j = 0
    max_type_index = []
    m = max(count_list)

    for i in count_list:
        if i==m:
            max_type_index.append(j)
        j+=1

    print("\nYour skin type might be:")
    for i in max_type_index:
        print(f"\n{type_list[i]}")
        for count, desc in enumerate(dictionary_skin.get(type_list[i])):
            print(f"{count+1}. {desc}")

def frequency():
    valid_input = False
    while not valid_input:
        tips = input("Share your beauty tips: ")
        valid_input = validate_skin_input(tips)

    words_tokenize = word_tokenize(tips)
    words_tagged = pos_tag(words_tokenize, tagset="universal")

    print("\nPart of speech words")
    for word in words_tagged:
        print(f"{word[0]}: {word[1]}")

    print("\nFrequency Distributions")
    freq_dist = FreqDist(words_tokenize)
    for fd, count in freq_dist.most_common():
        print(f"{fd}: {count}")

    user_input = ""
    while user_input is not "Y" and user_input is not "N":
        user_input = input("Do you want to show parse tree? [Y|N, case sensitive]: ")

    if user_input == "Y":
        ner = ne_chunk(words_tagged)
        ner.draw()
    else:
        pass

while(user_input!=3):
    print("\n=============")
    print("Skin Analyzer")
    print("=============")
    print("1. My Skin Type")
    print("2. Frequency")
    print("3. Exit")
    print(">>", end=" ")

    try:
        user_input = int(input())
    except Exception as e:
        user_input = 0
        print("That's not a number")

    if(user_input == 1):
        skin_type()
    elif(user_input == 2):
        frequency()
    elif(user_input == 3):
        print("Program is closing...")
        break