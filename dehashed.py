#!/usr/bin/env python3

import argparse
import requests
import json
from colorama import Fore, Style, init
init(autoreset=True)

API_KEY = '<YOUR API KEY>'

HEADERS = {
    'Content-Type': 'application/json',
    'Dehashed-Api-Key': API_KEY,
}

outfile = None
verbose = False


def write_output(data):
    with open(outfile, 'a') as of:
        of.write(str(data) + "\n")


def query_api(query, page=1, size=100, de_dupe=False, wildcard=False, regex=False):
    payload = {
        "query": query,
        "page": page,
        "size": size,
        "de_dupe": de_dupe,
        "wildcard": wildcard,
        "regex": regex,
    }
    try:
        res = requests.post('https://api.dehashed.com/v2/search', json=payload, headers=HEADERS)
        if res.status_code == 200:
            return res.json()
        else:
            print(Fore.RED + f'Error {res.status_code}: {res.text}')
            return None
    except Exception as e:
        print(Fore.RED + f'Exception: {e}')
        return None


def pp_json(data):
    formatted = json.dumps(data, sort_keys=True, indent=4)
    print(formatted)
    if outfile:
        write_output(formatted)


def parse_out(data):
    entries = data.get('entries', [])
    if not entries:
        print(Fore.YELLOW + 'No entries found.')
        return
    for entry in entries:
        for k, v in entry.items():
            print(Fore.CYAN + f'{k}' + Style.RESET_ALL + f' : {v}')
        print()
    if outfile:
        write_output(json.dumps(entries, indent=4))


def print_filtered(data, fields=['email', 'password', 'hashed_password']):
    entries = data.get('entries', [])
    if not entries:
        print(Fore.YELLOW + 'No entries found.')
        return
    for entry in entries:
        parts = []
        for field in fields:
            val = entry.get(field)
            if val:
                if isinstance(val, list):
                    parts.append(', '.join(str(v) for v in val))
                else:
                    parts.append(str(val))
            else:
                parts.append('')
        line = ' | '.join(parts)
        if line.strip(' |'):
            print(line)
            if outfile:
                write_output(line)


def main():
    global outfile, verbose

    parser = argparse.ArgumentParser(description='Tool to query the Dehashed v2 API.')
    parser.add_argument('-q', '--query', dest='query', type=str, help='Search query (e.g. domain:garrotxa.com)')
    parser.add_argument('-l', '--list', dest='query_list', type=str, default=None, help='File with list of queries.')
    parser.add_argument('-p', '--pretty', dest='pretty_out', action='store_true', default=False, help='Pretty print all fields per entry.')
    parser.add_argument('-f', '--fields', dest='fields', type=str, default=None, help='Campos a mostrar separados por coma: email,password,hashed_password,...')
    parser.add_argument('-o', '--out_file', dest='out_file', default=None, type=str, help='Guardar output a fichero.')
    parser.add_argument('-d', '--dedupe', dest='de_dupe', action='store_true', default=False, help='Eliminar duplicados.')
    parser.add_argument('--page', dest='page', type=int, default=1, help='Página de resultados.')
    parser.add_argument('--size', dest='size', type=int, default=100, help='Resultados por página (max 10000).')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose.')
    args = parser.parse_args()

    verbose = args.verbose
    outfile = args.out_file

    queries = []
    if args.query:
        queries.append(args.query)
    if args.query_list:
        with open(args.query_list, 'r') as f:
            queries += [line.strip() for line in f if line.strip()]

    if not queries:
        print(Fore.RED + 'Proporciona una query con -q o una lista con -l.')
        exit(1)

    for q in queries:
        print(Fore.GREEN + f'\n[*] Buscando: {q}')
        result = query_api(q, page=args.page, size=args.size, de_dupe=args.de_dupe)
        if result:
            total = result.get('total', 0)
            balance = result.get('balance', '?')
            print(Fore.YELLOW + f'Total: {total} resultados | Créditos restantes: {balance}')

            if args.fields:
                fields = [f.strip() for f in args.fields.split(',')]
                print(Fore.CYAN + ' | '.join(fields))
                print(Fore.CYAN + '-' * 60)
                print_filtered(result, fields=fields)
            elif args.pretty_out:
                parse_out(result)
            else:
                pp_json(result)


if __name__ == '__main__':
    main()
