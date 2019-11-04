
cz_months_map = {
    'leden': 'january',
    'únor': 'february',
    'březen': 'march',
    'duben': 'april',
    'květen': 'may',
    'červen': 'june',
    'červenec': 'july',
    'srpen': 'august',
    'září': 'september',
    'říjen': 'october',
    'listopad': 'november',
    'prosinec': 'december',
}

cz_weekdays = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek']
cz_weekday_map = {
    0: 'Pondělí',
    1: 'Úterý',
    2: 'Středa',
    3: 'Čtvrtek',
    4: 'Pátek',
    5: 'Sobota',
    6: 'Neděle',
}

def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
