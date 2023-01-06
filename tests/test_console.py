#!/usr/bin/python3
"""Test module for the console"""

import unittest
import os
import sys
from io import StringIO

from models import storage
from models.engine import classes
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """Tests for the console"""

    file_name = storage._FileStorage__file_path
    cmd = HBNBCommand()

    def remove_json(self):
        '''Removes the JSON file and reload'''
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        if storage.all():
            storage.reload()

    def execute(self, line):
        '''Executes a command line'''
        sys.stdout = StringIO()
        self.cmd.onecmd(line)

    def test_cls_name(self):
        """Tests for checking that cls name is entered and is valid"""
        self.remove_json()

        cls_missing = '** class name missing **'
        cls_not_found = "** class doesn't exist **"

        for command in ('create', 'destroy', 'show', 'update'):
            self.execute(command)
            self.assertEqual(sys.stdout.getvalue()[:-1], cls_missing)

            self.execute(f'.{command}()')
            self.assertEqual(sys.stdout.getvalue()[:-1], cls_missing)

            self.execute(f'{command} NoClass')
            self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)

            self.execute(f'NoClass.{command}()')
            self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)

        self.execute(f'all NoClass')
        self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)

        self.execute(f'NoClass.all()')
        self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)

        self.execute(f'NoClass.count()')
        self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)

        for do_cmd in (self.cmd.do_create, self.cmd.do_destroy,
                       self.cmd.do_show, self.cmd.do_update):
            sys.stdout = StringIO()
            do_cmd('')
            self.assertEqual(sys.stdout.getvalue()[:-1], cls_missing)

            sys.stdout = StringIO()
            do_cmd('NoClass')
            self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)

        sys.stdout = StringIO()
        self.cmd.do_all('NoClass')
        self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)

        sys.stdout = StringIO()
        self.cmd.do_count('NoClass')
        self.assertEqual(sys.stdout.getvalue()[:-1], cls_not_found)
        pass

    def test_id(self):
        """Tests for checking that id is entered and is valid"""
        self.remove_json()

        id_missing = '** instance id missing **'
        obj_not_found = '** no instance found **'

        for command in ('destroy', 'show', 'update'):
            for cls_name in classes.keys():
                self.execute(f'{cls_name}.{command}()')
                self.assertEqual(sys.stdout.getvalue()[:-1], id_missing)

                self.execute(f'{command} {cls_name}')
                self.assertEqual(sys.stdout.getvalue()[:-1], id_missing)

                self.execute(f'{cls_name}.{command}(xyz)')
                self.assertEqual(sys.stdout.getvalue()[:-1], obj_not_found)

                self.execute(f'{command} {cls_name} xyz')
                self.assertEqual(sys.stdout.getvalue()[:-1], obj_not_found)

        for do_cmd in (self.cmd.do_destroy, self.cmd.do_show,
                       self.cmd.do_update):
            for cls_name in classes.keys():
                sys.stdout = StringIO()
                do_cmd(f'{cls_name}')
                self.assertEqual(sys.stdout.getvalue()[:-1], id_missing)

                sys.stdout = StringIO()
                do_cmd(f'{cls_name} xyz')
                self.assertEqual(sys.stdout.getvalue()[:-1], obj_not_found)

    def test_create(self):
        """Tests for <create> command"""
        invalids = (r'aa="""', r'aa=""""', r'aa="\"""', r'aa="a1""', r"aa=''",
                    r'aa="\"', r'aa=\""', r'aa="\\"', r'aa==""', r'aa=xx',
                    r'aa="xx', r'aa=xx"', r'aa=1a1', r'aa=11a',  r'aa=a11',
                    r'aa=q.1', r'aa=1q.1', r'aa=q1.1', r'aa=1q2.1',
                    r'aa=0.z', r'aa=0.1z', r'aa=0.z1', r'aa=0.0z1',
                    r'aa=0..0')
        params = [r'a0="="', r'a1="\""', r'a2="\\""', r'a3="\"\""', r'a4=""',
                  r'a5="\"abc\""', r'a6="abc"', r'a7="abc_def"', r'a8="aa_"',
                  r'a9="abc_=_\"def\"_&_!\@#$%^&*&()_+=-"', r'a10="0123"',
                  r'a11="123.523"',
                  r'b0=0', r'b1=000', r'b2=+0', r'b3=-0', r'b4=01', r'b5=+01',
                  r'b6=123456789054656', r'b7=-123456789054656',
                  r'c0=0.0', r'c1=000.0', r'c2=0.000', r'c3=00.00',
                  r'c4=-0.0', r'c5=+00.00', r'c6=01.10', r'c7=+01.10',
                  r'c8=0.9', r'c9=89.0', r'c10=12345.09876',
                  r'c11=123456789054656.123456789054656',
                  r'c12=-123456789054656.123456789054656']
        outputs = [("a0", r'=', str), ("a1", r'"', str), ("a2", r'\"', str),
                   ("a3", r'""', str), ("a4", r'', str),
                   ("a5", r'"abc"', str), ("a6", r'abc', str),
                   ("a7", r'abc def', str), ("a8", r'aa ', str),
                   ("a9", r'abc = "def" & !\@#$%^&*&() +=-', str),
                   ("a10", r'0123', str), ("a11", r'123.523', str),
                   ("b0", 0, int), ("b1", 0, int), ("b2", 0, int),
                   ("b3", 0, int), ("b4", 1, int),  ("b5", 1, int),
                   ("b6", 123456789054656, int),
                   ("b7", -123456789054656, int),
                   ("c0", 0.0, float), ("c1", 0.0, float), ("c2", 0.0, float),
                   ("c3", 0.0, float), ("c4", 0.0, float), ("c5", 0.0, float),
                   ("c6", 1.1, float), ("c7", 1.1, float), ("c8", 0.9, float),
                   ("c9", 89.0, float), ("c10", 12345.09876, float),
                   ("c11", 123456789054656.123456789054656, float),
                   ("c12", -123456789054656.123456789054656, float)]
        for cls_name, cls in classes.items():
            self.remove_json()

            ids = []
            for line in (f'{cls_name}.create()', f'create {cls_name}'):
                self.execute(line)
                ids.append(sys.stdout.getvalue()[:-1])
            sys.stdout = StringIO()
            self.cmd.do_create(cls_name)
            ids.append(sys.stdout.getvalue()[:-1])

            for invalid in invalids:
                self.execute(f'create {cls_name} {invalid}')
                id = sys.stdout.getvalue()[:-1]
                ids.append(id)
                obj = storage.all()['.'.join((cls_name, id))]
                self.assertIsNone(getattr(obj, "aa", None))

            self.execute(f'create {cls_name} {" ".join(params)}')
            id = sys.stdout.getvalue()[:-1]
            ids.append(id)
            obj = storage.all()['.'.join((cls_name, id))]
            for attr, val, val_type in outputs:
                value = getattr(obj, attr, None)
                self.assertIsNotNone(value)
                self.assertIsInstance(value, val_type)
                self.assertEqual(value, val)

            for id in ids:
                index = '.'.join((cls_name, id))
                self.assertIn(index, storage.all().keys())
                self.assertIsInstance(storage.all()[index], cls)

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_show(self):
        """Tests for <show> command"""
        self.remove_json()

        for cls_name, cls in classes.items():

            obj = cls()
            id = obj.id
            index = '.'.join((cls_name, id))

            for line in (f'{cls_name}.show({id})', f'show {cls_name} {id}'):
                self.execute(line)
                self.assertEqual(sys.stdout.getvalue()[:-1], str(obj))

            sys.stdout = StringIO()
            self.cmd.do_show(f'{cls_name} {id}')
            self.assertEqual(sys.stdout.getvalue()[:-1], str(obj))

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_destroy(self):
        """Tests for <destroy> command"""
        self.remove_json()

        for cls_name, cls in classes.items():

            objs = [cls() for i in range(3)]
            ids = [obj.id for obj in objs]
            indices = ['.'.join((cls_name, id)) for id in ids]
            commands = (f'{cls_name}.destroy' + '({})',
                        f'destroy {cls_name} ' + '{}')

            for i in range(2):
                self.assertIn(indices[i], storage.all().keys())
                self.execute(commands[i].format(ids[i]))
                self.assertNotIn(indices[i], storage.all().keys())

            sys.stdout = StringIO()
            self.assertIn(indices[2], storage.all().keys())
            self.cmd.do_destroy(f'{cls_name} {ids[2]}')
            self.assertNotIn(indices[2], storage.all().keys())

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_all(self):
        """Tests for <all> command"""
        self.remove_json()

        sys.stdout = StringIO()
        self.cmd.onecmd('all')
        self.assertEqual(sys.stdout.getvalue()[:-1], '[]')

        for cls_name, cls in classes.items():
            for line in (f'{cls_name}.all()', f'all {cls_name}'):
                self.execute(line)
                self.assertEqual(sys.stdout.getvalue()[:-1], '[]')

        all_objs = []
        for cls_name, cls in classes.items():
            n = 5
            objs = [cls() for i in range(n)]
            all_objs += objs

            outputs = []
            for line in (f'{cls_name}.all()', f'all {cls_name}'):
                self.execute(line)
                outputs.append(sys.stdout.getvalue()[:-1])
            sys.stdout = StringIO()
            self.cmd.do_all(cls_name)
            outputs.append(sys.stdout.getvalue()[:-1])

            for out in outputs:
                for obj in objs:
                    self.assertTrue(out.find(str(obj)) > 0)
                    self.assertEqual(out[0], '[')
                    self.assertEqual(out[-1], ']')

        outputs = []
        self.execute('all')
        outputs.append(sys.stdout.getvalue()[:-1])

        sys.stdout = StringIO()
        self.cmd.do_all('')
        outputs.append(sys.stdout.getvalue()[:-1])

        for out in outputs:
            for obj in all_objs:
                self.assertTrue(out.find(str(obj)) > 0)
                self.assertEqual(out[0], '[')
                self.assertEqual(out[-1], ']')

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_update(self):
        """Tests for <update> command"""
        self.remove_json()

        attrib_missing = '** attribute name missing **'
        value_missing = '** value missing **'
        for cls_name, cls in classes.items():
            obj = cls()
            id = obj.id

            for line in (f'update {cls_name} {id}',
                         f'{cls_name}.update({id})',
                         f'{cls_name}.update({id}, {{}})'):
                self.execute(line)
                self.assertEqual(sys.stdout.getvalue()[:-1], attrib_missing)

            sys.stdout = StringIO()
            self.cmd.do_update(f'{cls_name} {id}')
            self.assertEqual(sys.stdout.getvalue()[:-1], attrib_missing)

            for line in (f'update {cls_name} {id} name',
                         f'{cls_name}.update({id}, name)',
                         f'{cls_name}.update({id}, {{name: }})'):
                self.execute(line)
                self.assertEqual(sys.stdout.getvalue()[:-1], value_missing)

            sys.stdout = StringIO()
            self.cmd.do_update(f'{cls_name} {id} name')
            self.assertEqual(sys.stdout.getvalue()[:-1], value_missing)

            values = ['hello', 'hello, world']
            res = [val.split(', ')[0] for val in values]
            for line in (f'update {cls_name} {id} test ' + '{}',
                         f'{cls_name}.update({id}, test, ' + '{})'):
                for i in range(len(values)):
                    self.execute(line.format(values[i]))
                    self.assertEqual(obj.test, res[i])
                    self.assertIn('test', obj.to_dict())

            res = values
            for line in (f'update {cls_name} {id} test ' + '"{}"',
                         f'{cls_name}.update({id}, test, ' + '"{}")'):
                for i in range(len(values)):
                    self.execute(line.format(values[i]))
                    self.assertEqual(obj.test, res[i])
                    self.assertIn('test', obj.to_dict())

            sys.stdout = StringIO()
            self.cmd.do_update(f'{cls_name} {id} x1 y2')
            self.assertEqual(obj.x1, 'y2')
            self.assertIn('x1', obj.to_dict())

            attr_dicts = [{'One_attr': 'Its value'},
                          {'test1': 'True', 'test2': 'False'}]
            line = f'{cls_name}.update({id}, ' + '{})'
            for d in attr_dicts:
                self.execute(line.format(d))
                for attr, val in d.items():
                    self.assertEqual(getattr(obj, attr), val)
                    self.assertIn(attr, obj.to_dict())

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_count(self):
        """Tests for <class_name>.count() command"""
        self.remove_json()

        for cls_name, cls in classes.items():
            self.execute(f'{cls_name}.count()')
            self.assertEqual(sys.stdout.getvalue()[:-1], '0')

        all_objs = []
        for cls_name, cls in classes.items():
            n = 5
            objs = [cls() for i in range(n)]
            all_objs += objs

            self.execute(f'{cls_name}.count()')
            self.assertEqual(sys.stdout.getvalue()[:-1], str(n))

        self.remove_json()
        sys.stdout = sys.__stdout__
        pass

    def test_EOF(self):
        """Tests for <EOF> command"""
        sys.stdout = StringIO()
        HBNBCommand().onecmd('EOF')
        self.assertEqual(sys.stdout.getvalue(), '\n')
        sys.stdout = sys.__stdout__
        pass

    def test_quit(self):
        """Tests for <quit> command"""
        sys.stdout = StringIO()
        HBNBCommand().onecmd('quit')
        self.assertEqual(sys.stdout.getvalue(), '')
        sys.stdout = sys.__stdout__
        pass

    def test_blank_line(self):
        """Tests for blank lines"""
        sys.stdout = StringIO()
        HBNBCommand().onecmd('')
        self.assertEqual(sys.stdout.getvalue(), '')
        sys.stdout = sys.__stdout__
        pass

    def test_help(self):
        """Tests for <help> command"""
        f = sys.stdout = StringIO()
        HBNBCommand().onecmd('help quit')
        self.assertEqual(f.getvalue()[:-1],
                         '\n\tquit:\t\t\tExits the program\n')
        pass
    pass
