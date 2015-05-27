import ConfigParser
import os
import time
from ConfigParser import NoOptionError
import codecs

class Configuration(object):
    """ Generator configuration file handling """
    
    def __init__(self):
        self.fable_id = None
        self.ebook_format = None
        self.lang = None
        self.sex = None
        self.name = None
        self.birthdate = None
        self.dedication = None
        
    def read(self, configuration_file):
        print '-- Reading configuration file: ', configuration_file
        self._read_configuration(configuration_file)
        return self._validate_args()
    
    def _get_item(self, parser, itemname):
        value = None
        try:
            value = parser.get('eBook',itemname)
        except NoOptionError:
            pass
        return value
        
    def _read_configuration(self, configuration_file):
        config_items = None
        try:
            parser = ConfigParser.SafeConfigParser(allow_no_value=False)
            parser.readfp(codecs.open(configuration_file, "r", "utf-8"))
            self.fable_id = self._get_item(parser, 'fable_id')
            self.ebook_format = self._get_item(parser, 'format').upper()
            self.lang = self._get_item(parser, 'language').upper()
            self.sex = self._get_item(parser, 'sex').upper()
            self.name = self._get_item(parser, 'name')
            self.birthdate = self._get_item(parser, 'birthdate')
            self.dedication = self._get_item(parser, 'dedication')
        except IOError as ioex:
            print '** ERROR: Cannot read configuration file: ' + configuration_file
            print '** ', os.strerror(ioex.errno)
        return config_items
            
    def _validate_args(self):
        validate_ok = True
        try:
            fable_id = int(self.fable_id)
        except:
            print 'Invalid fable id %s' % self.fable_id
            return False
        if fable_id <0 or fable_id > 8:
            print 'Invalid fable id %s' % self.fable_id
            print 'Valid choices are: 0-1-2-3-4-5-6-7-8'
            print
            validate_ok = False
        elif self.lang != 'EN' and self.lang != 'IT' and self.lang != 'RO':
            print 'Unknown lang %s' % self.lang
            validate_ok = False
        elif self.sex != 'M' and self.sex != 'F':
            print 'Invalid sex param. Valid choices are M or F.'
            validate_ok = False
        elif self.name is None or len(self.name)<=1:
            print 'Invalid name.'
            validate_ok = False
        elif self.birthdate is not None:
            if len(self.birthdate) != 9:
                print 'Invalid birthdate. Must be 9 characters, ie: 26-Aug-80'
                validate_ok = False
            try:
                time.strptime(self.birthdate, "%d-%b-%y")
            except:
                print 'Cannot parse birthdate. Invalid format? Must be dd-mmm-yy'
                validate_ok = False
        elif self.ebook_format != 'EPUB' and self.ebook_format != 'PDF':
            print 'Invalid format. It must be either PDF or EPUB'
            validate_ok = False
        return validate_ok
