import requests ## to communicate 
import hashlib ## to create encripted psswrd info
import sys ## to parse arguments


def request_api_data(query_chars:str):
    assert type(query_chars) == str
    API_URL = 'https://api.pwnedpasswords.com/range/'
    res = requests.get(API_URL+query_chars)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again!')
    return res 

def get_psswrd_leaks_count(hashes_candidates_tail, hash_to_check:str):
    hashes = (line.split(':') for line in hashes_candidates_tail.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(real_pswrd:str):
    sha1_psswrd = hashlib.sha1(real_pswrd.encode('utf-8')).hexdigest().upper()
    first_5_char, tail =  sha1_psswrd[:5], sha1_psswrd[5:]
    response = request_api_data(first_5_char)
    return get_psswrd_leaks_count(response, tail)

def main(args:list):
    for psswrd in args:
        count = pwned_api_check(psswrd)
        if count:
            print(f'{psswrd} was found {count} times. You shouldn\'t use this password!')
        else:
            print(f'{psswrd} was not found. Carry on using this one!')

    return 'Done! Program finishing...'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:])) ## to access as many arguments as we want to pass