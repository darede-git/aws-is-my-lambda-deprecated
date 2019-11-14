import boto3
import os
from datetime import datetime
import re

AWS_PROFILE = os.getenv('AWS_PROFILE')
session = boto3.Session(profile_name=AWS_PROFILE)


def get_regions():
    ec2 = session.client('ec2')
    regions = ec2.describe_regions()
    return [name.get('RegionName') for name in regions.get('Regions')]


def get_lambdas():
    ret = []
    for regiao in get_regions():
        client = session.client('lambda', region_name=regiao)
        response = client.list_functions()
        if len(response.get('Functions')) > 0:
            for func in response.get('Functions'):
                ret.append(create_lambda(func, regiao))
    return ret


def create_lambda(lin, region):
    return {'Name': lin.get('FunctionName'), 'Runtime':  lin.get('Runtime'), 
            'Arn': lin.get('FunctionArn'), 'Region':region}


def get_version(text):
    ret = re.findall(r'\d', text)
    return ret


def check_version(func):
    ver = get_version(func.get('Runtime'))
    if 'python' in func.get('Runtime'):
        return False if int(ver[0]) < 3 else True
    elif 'node' in func.get('Runtime'):
        return False if int(ver[0]) < 10 else True
    else:
        return True


def get_warnings():
    ret = []
    lambdas = get_lambdas()
    if len(lambdas) > 0:
        for func in lambdas:
            if not check_version(func):
                ret.append(func)
    return ret


def main():
    warns = get_warnings()
    for func in warns:
        print('Function "{}" running on region "{}" is using "{}".'.format(
                  func.get('Name'), func.get('Region'), func.get('Runtime')
              ) + ' Please, consider update it to a newer runtime!')


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))