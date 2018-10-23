'''
ACI APIC AppCreator

@contact: aciappcenter-support@cisco.com
@version: 1.1
'''
from __future__ import print_function

import argparse
import json
import os
import re
import readline
import shutil
import signal
import sys

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))

import logging
import aci_app_validator
import aci_app_packager

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def bold(text):
        return '{}{}{}'.format(bcolors.BOLD, text, bcolors.ENDC)

    @staticmethod
    def header(text):
        return '{}{}{}'.format(bcolors.HEADER, text, bcolors.ENDC)

    @staticmethod
    def blue(text):
        return '{}{}{}'.format(bcolors.OKBLUE, text, bcolors.ENDC)

    @staticmethod
    def green(text):
        return '{}{}{}'.format(bcolors.OKGREEN, text, bcolors.ENDC)

    @staticmethod
    def warning(text):
        return '{}{}{}'.format(bcolors.WARNING, text, bcolors.ENDC)

    @staticmethod
    def fail(text):
        return '{}{}{}'.format(bcolors.FAIL, text, bcolors.ENDC)



SCRIPT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_DIR = os.path.join(SCRIPT_DIR_PATH, 'AppTemplate')
STATELESS_TEMPLATE_DIR  = os.path.join(TEMPLATE_DIR, 'StatelessAppTemplate')
STATEFUL_TEMPLATE_DIR   = os.path.join(TEMPLATE_DIR, 'StatefulAppTemplate')
STATEFULJS_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'StatefulJS')

ACI_PACKAGER_PATH = os.path.join(SCRIPT_DIR_PATH, 'aci_app_packager.py')

if not os.path.isfile(ACI_PACKAGER_PATH):
    print(bcolors.fail('Packager not found ({0})'.format(SCRIPT_DIR_PATH)))
    sys.exit(1)


class MandatoryFieldsTemplate(object):
    fields = {
        'version': '1.0',
        'name': 'MyApp',
        'shortdescr': 'My first ACI app',
        'vendor': 'Vendor',
        'apicversion': '2.2(1n)',
        'permissions': ['admin'],
        'permissionslevel': 'read',
        'author': 'Author',
        'category': ['Beta'],
        'contact-phone': '123-4567890',
        'contact-url': 'http://www.cisco.com/go/aci',
        'contact-email': 'aci-devnet@external.cisco.com'
    }

    def __init__(self, arg):
        super(MandatoryFieldsTemplate, self).__init__()

    @classmethod
    def getFields(cls):
        return cls.fields


MANDATORY_FIELDS_DESCRIPTION = {
    'version': 'Format: M.m',
    'name': 'App name',
    'shortdescr': 'Description',
    'vendor': 'Vendor name',
    'apicversion': 'Min APIC version',
    'permissions': 'Permissions required, let field empty when finished',
    'permissionslevel': 'read/write',
    'author': 'Author(s)',
    'category': 'Category'
}

MANDATORY_FIELDS_STATEFUL_DESCRIPTION = {
    'api': 'API description'
}

OPTIONAL_FIELDS_DESCRIPTION = {
    'contact': 'Contact'
}


# Validating functions

def validator_factory(json_dict):
    validator = aci_app_validator.Validator()
    validator.appMeta = json_dict

    return validator


def validate_field(field, value, state='stateless'):
    if field == 'contact-email' or field == 'contact-url' or field == 'contact-phone':
        return aci_app_validator.Validator.validateJsonFieldsDuringGeneration({'contact': {field: value}}, state)
    return aci_app_validator.Validator.validateJsonFieldsDuringGeneration({field: value}, state)


# App creation functions

def output_directory_path(parent_out_dir, vendordomain, appid):
    return os.path.join(parent_out_dir, '{0}_{1}'.format(vendordomain, appid))

def file_replace(fname, pat, s_after):
    # first, see if the pattern is even in the file.
    with open(fname) as f:
        if not any(re.search(pat, line) for line in f):
            return  # pattern does not occur in file so we are done.

    # pattern is in the file, so perform replace operation.
    with open(fname) as f:
        out_fname = fname + ".tmp"
        out = open(out_fname, "w")
        for line in f:
            out.write(re.sub(pat, s_after, line))
        out.close()

    try:
        os.rename(out_fname, fname)
    except:
        os.remove(fname)
        os.rename(out_fname, fname)


# Read file
def read_content_file(fname):
    s = ''
    with open(fname, 'r') as f:
        s = str(f.read())
    return s


def copy_structure(app, misc):
    state = misc['state']
    outdir = misc['output_dir']
    protocol = misc['protocol']

    output_dir = ''

    if outdir:
        if not os.path.isdir(outdir):
            raise Exception('Output directory doesn\'t exist')

        output_dir = output_directory_path(outdir, app['vendordomain'], app['appid'])
    else:
        output_dir = output_directory_path(SCRIPT_DIR_PATH, app['vendordomain'], app['appid'])

    shutil.copytree(STATELESS_TEMPLATE_DIR, output_dir)

    if state == 'stateful':
        files_in_stateful_dir = os.listdir(STATEFUL_TEMPLATE_DIR)
        for item in files_in_stateful_dir:
            path = os.path.join(STATEFUL_TEMPLATE_DIR, item)
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(output_dir, item))
    
    uiassets_path = os.path.join(output_dir, 'UIAssets')
    apphtml_path  = os.path.join(uiassets_path, 'app.html')
    file_replace(apphtml_path, '{{VENDORDOMAIN}}', app['vendordomain'])
    file_replace(apphtml_path, '{{APPID}}', app['appid'])
    file_replace(apphtml_path, '{{APPNAME}}', app['name'])

    if state == 'stateful':
        service_path  = os.path.join(output_dir, 'Service')
        serverpy_path = os.path.join(service_path, 'server.py')
        file_replace(serverpy_path, '{{VENDORDOMAIN}}', app['vendordomain'])
        file_replace(serverpy_path, '{{APPID}}', app['appid'])
        file_replace(serverpy_path, '{{PROTOCOL}}', protocol)

        query_url = 'window.BACKEND_QUERY_URL = location.protocol + "//" + window.location["host"] + "/appcenter/{}/{}";'.format(
            app['vendordomain'], app['appid'])
        file_replace(apphtml_path, '{{BACKEND_QUERY_URL}}', query_url)

        testAPI = read_content_file(os.path.join(STATEFULJS_TEMPLATE_DIR, 'testAPI.html'))
        file_replace(apphtml_path, '{{TEST_API}}', testAPI)

        getTenant = read_content_file(os.path.join(STATEFULJS_TEMPLATE_DIR, 'getTenant.html'))
        file_replace(apphtml_path, '{{GET_TENANT}}', getTenant)

        alerts = read_content_file(os.path.join(STATEFULJS_TEMPLATE_DIR, 'alerts.html'))
        file_replace(apphtml_path, '{{ALERTS_STATEFUL}}', alerts)

        app['api'] = {}
        app['api']['testAPI.json'] = "API to test the connectivity to the docker container."
        app['api']['getTenant.json'] = "Get the list of the tenants in the docker container."

    else:
        file_replace(apphtml_path, '{{BACKEND_QUERY_URL}}', '')
        file_replace(apphtml_path, '{{TEST_API}}', '')
        file_replace(apphtml_path, '{{GET_TENANT}}', '')
        file_replace(apphtml_path, '{{ALERTS_STATEFUL}}', '')

    app_json_file = os.path.join(output_dir, 'app.json')
    with open(app_json_file, 'w+') as appfile:
        appfile.write(json.dumps(app, indent=4))

    return output_dir


# Input functions

def input_custom_msg(msg):
    if msg:
        return raw_input('> {} '.format(msg))
    else:
        return raw_input('> ')


def input_line():
    return input_custom_msg('')


def input_with_check(msg, check_fct, error_msg):
    inp = ''
    inp_correct = False
    while not inp_correct:
        inp = input_custom_msg(msg)
        if not check_fct(inp):
            print(bcolors.fail(error_msg))
        else:
            inp_correct = True
    return inp


def yes_no_input():
    def check_y_n(inp):
        return inp and (inp.lower() == 'y' or inp.lower() == 'n')

    return input_with_check('(y/n)', check_y_n, '"y"(es) or "n"(o)')


def input_check_json_field(field, state='stateless', skip_possible=False, custom_msg=''):
    inp = ''
    inp_correct = False
    while not inp_correct:
        inp = input_custom_msg(custom_msg)
        if skip_possible and not inp:
            inp_correct = True
        else:
            err_code = 0
            err_msg = ''

            if field == 'permissions':
                err_code, err_msg = validate_field(field, [inp], state)
            else:
                err_code, err_msg = validate_field(field, inp, state)

            if err_code != 0:
                print(bcolors.fail(err_msg))
            else:
                inp_correct = True
    return inp


### Packaging

def package_app(app_directory, output_dir):
    #return os.system("python {0} -f {1}".format(ACI_PACKAGER_PATH, app_directory))
    packager = aci_app_packager.Packager()
    return packager.main(app_directory, SCRIPT_DIR_PATH, output_dir)

if __name__ == '__main__':
    output_dir = ''  # Where to output the app
    appid = ''  # appid, unique identifier of the app
    vendordomain = ''  # Organization
    state = ''  # 'staless' or 'stateful' (contains docker image)
    protocol = ''  # HTTPS or HTTP

    parser = argparse.ArgumentParser()

    parser._optionals.title = 'Optional arguments'

    parser.add_argument('-o', '--output', help='Output directory', default='')
    args = vars(parser.parse_args())

    output_dir = ''
    if not args['output']:
        output_dir = SCRIPT_DIR_PATH
    else:
        output_dir = args['output']

    if not os.path.isabs(output_dir):
        output_dir = os.path.join(os.getcwd(), output_dir)

    # Init the fields
    fields = {}
    fields['iconfile'] = 'icon.png'

    # Title
    print(bcolors.header('*******************************************'))
    print(bcolors.bold(bcolors.header('*             ACI App Creator             *')))
    print(bcolors.header('*******************************************'))

    print('Welcome! This tool will guide you through the creation of a fully functional ACI App Center application.')
    print('The information that you will provide can be changed later on, please read the ACI App Center Developer '
          'Guide to learn more about it.')
    print('')

    print(bcolors.header('--- General information ---'))

    print(bcolors.bold('Let\'s begin! What should be the name of your application? (e.g. "TestingApp", "MyFirstApp",'
                       '...)'))
    print('Note: The name of the application will also be used as the application ID.\nThis can be changed afterwards '
          'in "app.json".')
    fields['name'] = input_check_json_field('appid', custom_msg='(Application name)')
    fields['appid'] = fields['name']

    print('')

    print(bcolors.bold('What is the name of your company?'))
    print('Note: The company name will also be used as the vendor domain.\nThis can be changed afterwards in '
          '"app.json".')
    fields['vendor'] = input_check_json_field('vendordomain', custom_msg='(Company name)')
    fields['vendordomain'] = fields['vendor']

    # Check if output directory exists    
    output_test = output_directory_path(output_dir, fields['vendordomain'], fields['appid'])

    if os.path.exists(output_test):
        print(bcolors.fail('The output directory ({0}) already exists...'.format(output_test)))
        sys.exit(1)

    print('')

    print(bcolors.bold('Can you describe briefly what the application is supposed to do?'))
    print('To skip it, leave the field empty. The following description will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['shortdescr'])))
    fields['shortdescr'] = input_check_json_field('shortdescr', custom_msg='(Description)', skip_possible=True)
    if not fields['shortdescr']:
        fields['shortdescr'] = MandatoryFieldsTemplate.getFields()['shortdescr']

    print('')

    print(bcolors.header('--- About you ---'))

    print(bcolors.bold('What is your name?'))
    fields['author'] = input_check_json_field('author', custom_msg='(Author)')

    print('')

    fields['contact'] = {}

    print(bcolors.bold('What is your email address?'))
    print('To skip it, leave the field empty. The following email address will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['contact-email'])))
    fields['contact']['contact-email'] = input_check_json_field('contact-email', custom_msg='(Email)',
                                                                skip_possible=True)
    if not fields['contact']['contact-email']:
        fields['contact']['contact-email'] = MandatoryFieldsTemplate.getFields()['contact-email']
    print('')

    print(bcolors.bold('What is the website of your company?'))
    print('To skip it, leave the field empty. The following website will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['contact-url'])))
    fields['contact']['contact-url'] = input_check_json_field('contact-url', custom_msg='(URL)', skip_possible=True)
    if not fields['contact']['contact-url']:
        fields['contact']['contact-url'] = MandatoryFieldsTemplate.getFields()['contact-url']
    print('')

    print(bcolors.bold('What is the contact phone number of your company?'))
    print('To skip it, leave the field empty. The following phone will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['contact-phone'])))
    fields['contact']['contact-phone'] = input_check_json_field('contact-phone', custom_msg='(Phone)',
                                                                skip_possible=True)
    if not fields['contact']['contact-phone']:
        fields['contact']['contact-phone'] = MandatoryFieldsTemplate.getFields()['contact-phone']
    print('')

    print(bcolors.header('--- App versions ---'))

    print(bcolors.bold('Would you like to change the version of the application?'))
    print('To skip it, leave the field empty. The following version will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['version'])))

    fields['version'] = input_check_json_field('version', custom_msg='(Version, the format is: Major.Minor)',
                                               skip_possible=True)
    if not fields['version']:
        fields['version'] = MandatoryFieldsTemplate.getFields()['version']

    print('')

    print(bcolors.bold('Would you like to change the mininum APIC version on which the application can run?'))
    print('To skip it, leave the field empty. The following APIC version will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['apicversion'])))

    fields['apicversion'] = input_check_json_field('apicversion',
                                                   custom_msg='(Min APIC version, the format is: Major.Minor(mp), where m=maintenance and p=patch)',
                                                   skip_possible=True)
    if not fields['apicversion']:
        fields['apicversion'] = MandatoryFieldsTemplate.getFields()['apicversion']

    print('')

    print(bcolors.header('--- Permissions ---'))

    print(bcolors.bold('What permissions would you like the application to have?'))
    print(
        'Read more at this address: http://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/kb/b_KB_AAA-RBAC-roles-privileges.html')
    print('To skip it, leave the field empty. The following permissions will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['permissions'])))

    fields['permissions'] = []
    while True:
        inp = input_check_json_field('permissions', custom_msg='(Permission)', skip_possible=True)

        if len(fields['permissions']) == 0 and not inp:
            fields['permissions'] = MandatoryFieldsTemplate.getFields()['permissions']
            break
        elif not inp:
            break
        else:
            fields['permissions'].append(inp)

    err_code, err_msg = validate_field('permissions', fields['permissions'])
    if err_code != 0:
        print(bcolors.fail(err_msg))
    else:
        inp_correct = True

    print('')

    print(bcolors.bold('Should the application run with read or write priviledges?'))
    print('To skip it, leave the field empty. The following priviledge will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['permissionslevel'])))

    fields['permissionslevel'] = input_with_check('(Priviledge)',
                                                  lambda inp: inp == '' or inp == 'read' or inp == 'write',
                                                  'The input should be "read" or "write"')
    if not fields['permissionslevel']:
        fields['permissionslevel'] = MandatoryFieldsTemplate.getFields()['permissionslevel']

    print('')

    print(bcolors.header('--- Categories ---'))

    categories = ['Tools and Utilities',
                  'Visibility and Monitoring',
                  'Optimization',
                  'Security',
                  'Networking',
                  'Cisco Automation and Orchestration',
                  'Beta']

    print(bcolors.bold('Here are different categories:'))
    print('')
    print(bcolors.bold('\n'.join(categories)))
    print('')

    print(bcolors.bold('Please select the category(ies) which is(are) the most suitable for your app:'))
    print('If none of the categories are selected, the following category will be used: "{}"'.format(
        bcolors.blue(MandatoryFieldsTemplate.getFields()['category'])))

    fields['category'] = []

    for i in xrange(0, len(categories)):
        inp = input_with_check('({}, y/n)'.format(categories[i]),
                               lambda x: x and (x.lower() == 'y' or x.lower() == 'n'), '"y"(es) or "n"(o)')
        if inp == 'y':
            fields['category'].append(categories[i])

    if len(fields['category']) == 0:
        fields['category'] = MandatoryFieldsTemplate.getFields()['category']

    print('')

    print(bcolors.header('--- Other ---'))
    print(bcolors.bold('Would you like to add a docker container to your application?'))
    print(
        'Note: There are 2 kinds of apps: "{0}" and "{1}": \n - A stateless app is only composed of a front-end part, '
        'it communicates with the APIC without keeping any state. \n - A stateful app have a back-end (docker '
        'container) to keep a state amongst multiple launches of the app.'.format(
            bcolors.bold('stateless'), bcolors.bold('stateful')))

    inp = yes_no_input()

    print('\n')

    if inp.lower() == 'y':
        state = 'stateful'

        print(bcolors.bold('Will the container communicate with the APIC using HTTPS?'))
        print('Note: If no, HTTP will be used.')
        inp_https = yes_no_input()
        protocol = 'https' if inp_https.lower() == 'y' else 'http'

    else:
        state = 'stateless'

    err_code, err_msg = aci_app_validator.Validator.validateJsonFieldsDuringGeneration(fields, state)

    if err_code != 0:
        print(bcolors.fail('Validation failed: {}'.format(err_msg)))
        sys.exit()

    print('\n')
    print(bcolors.green('We are now creating your fully functional app in this directory: {}...\n'.format(output_dir)))

    app_directory = copy_structure(fields, {'state': state, 'output_dir': output_dir, 'protocol': protocol})

    print(bcolors.green('The application has been successfully created.'))
    print(
        'Don\'t forget, you can modify the content of the directory and repackage the app using the command "python '
        'aci_app_packager.py -f {}"'.format(
            app_directory))

    print('\n')
    print(bcolors.header('--- Packaging ---'))
    print(bcolors.bold('Would you like to package the app?'))
    print('This will create a .aci application.')

    inp = yes_no_input()
    if inp.lower() == 'y':
        rc = package_app(app_directory, output_dir)
        if rc != 0:
            print(bcolors.fail('Packaging of the application failed.'))
