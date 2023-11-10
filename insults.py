import random
# made to shorten the main.py file since it's literally spaghetti code, my bad

def getInsult():
    insult = ""
    choice = random.randint(0, 10)

    match choice:
        case 0:
            insult = "bitch, stfu"
        case 1:
            insult = "your rights have been removed, dumbass"
        case 2:
            insult = "little baby shithead, you gonna cry? you gonna cry me a river? are you having a big sad?"
        case 3:
            insult = "aww, you forgot, didn't you? prick"
        case 4:
            insult = "goddammit, did your mother drop you as a child, or are you just stupid?"
        case 5:
            insult = "why the FUCK are you still here, baby bitch?"
        case 6:
            insult = "get your bitch ass motherfucking dickhead ass out of here"
        case 7:
            insult = "this just in, you're a fucking dumbass, and ive come to the conclusion you're also an asshat"
        case 8:
            insult = "man i'd wipe my brown ass with you"
        case 9: 
            insult = "who the fuck decided you needed to be here? not me!"
        case 10:
            insult = "your iq has a match! of a goldfish! asshat prick, no one likes you anyways"
    return insult

def getKidFriendlyInsult():
    insult = ""
    choice = random.randint(0, 10)

    match choice:
        case 0:
            insult = "shut up"
        case 1:
            insult = "your rights have been removed"
        case 2:
            insult = "you gonna cry? you gonna cry me a river? are you having a big sad?"
        case 3:
            insult = "aww, you forgot, didn't you?"
        case 4:
            insult = "stupid, love you"
        case 5:
            insult = "please leave"
        case 6:
            insult = "get out of here"
        case 7:
            insult = "this just in, you're a big dumb, and ive come to the conclusion you're also insecure"
        case 8:
            insult = "man i'd put you in the zoo"
        case 9: 
            insult = "who decided you needed to be here? not me!"
        case 10:
            insult = "your iq has a match! of a goldfish!"
    return insult

def getMixedInsult():
    insult = ""
    choice = random.randint(0, 10)

    match choice:
        case 0:
            insult = "bitch, stfu"
        case 1:
            insult = "your rights have been removed, dumbass"
        case 2:
            insult = "little baby shithead, you gonna cry? you gonna cry me a river? are you having a big sad?"
        case 3:
            insult = "aww, you forgot, didn't you? prick"
        case 4:
            insult = "goddammit, did your mother drop you as a child, or are you just stupid?"
        case 5:
            insult = "why the FUCK are you still here, baby bitch?"
        case 6:
            insult = "get your bitch ass motherfucking dickhead ass out of here"
        case 7:
            insult = "this just in, you're a fucking dumbass, and ive come to the conclusion you're also an asshat"
        case 8:
            insult = "man i'd wipe my brown ass with you"
        case 9: 
            insult = "who the fuck decided you needed to be here? not me!"
        case 10:
            insult = "your iq has a match! of a goldfish! asshat prick, no one likes you anyways"
        case 11:
            insult = "shut up"
        case 12:
            insult = "your rights have been removed"
        case 13:
            insult = "you gonna cry? you gonna cry me a river? are you having a big sad?"
        case 14:
            insult = "aww, you forgot, didn't you?"
        case 15:
            insult = "stupid, love you"
        case 16:
            insult = "please leave"
        case 17:
            insult = "get out of here"
        case 18:
            insult = "this just in, you're a big dumb, and ive come to the conclusion you're also insecure"
        case 19:
            insult = "man i'd put you in the zoo"
        case 20: 
            insult = "who decided you needed to be here? not me!"
        case 21:
            insult = "your iq has a match! of a goldfish!"
    return insult