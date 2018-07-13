from brasil import BrasilIO


def format_cnpj(root):
    assert len(root) == 8
    return f'{root[:2]}.{root[2:5]}.{root[-3:]}/xxx-xx'


api = BrasilIO()
cnpj = '02404361000129'  # ODEBRECHT SERVICOS DE INFRA-ESTRUTURA S/A
holdings = api.holdings(cnpj)

for company in holdings:
    family = api.family(company['cnpj_root'])
    total = len(family)
    print(f'{format_cnpj(company["cnpj_root"])} {company["nome"]} ({total} family members)')
    for member in family:
        print(f'  {format_cnpj(member["cnpj_root"])} {member["nome"]}')
    print()
