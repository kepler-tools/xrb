"""
A TemplateFile implements a very common practice of having a template of a
file's text that is then populated with some user data and rendered, or a
rendered file can be read in to extract the data.
"""
# TODO: determine dependencies/version reqs
#   Uses OrderedDict, which means 2.7+ without more work.  Note for 3.7+ all
#   dicts are ordered.

# NOTE: While mature Python Templating engines exist, when I did a quick review
# the general convention seems to have a set of data (e.g. in a dict) that is
# substituted into a text template (rendered).  That is half of what I want to
# do.  I also want to be able to read in a file that has already been rendered
# and use it to populate the data.  This may exist, but it wasn't clear how to
# do this in less time with Python builtins or mature templating engines.  May
# want to revisit this after prototyping.

# TODO: I've just made a basic class, but I could subclass the builtin File
# type.  After prototyping, check if this offers benefits.

# TODO: How should line regexes work on lines with more than one sub descriptor?
#   As of now, it is assumed all descriptors on the same line have the same line
#   regex

# TODO: I kinda abuse Formatter in this class.  Maybe worth it to write a
# Formatter subclass?

# TODO: Allow users to give a format-spec for each field for rendering

class TemplateFile(object):
    """Represents a template file."""

    def __init__(self, template_text):
        """Construct a TemplateFile

        Arguments:
            template_text    --> A template of the file's content, with
                                 substitution descriptors of the form 
                                 {field[line_regex]:field_regex} (see below).

        Substitution descriptors:
            The template_text can contain substitution descriptors used to both
            render a file and to interpret a rendered file. They are of the form
                {field[line_regex]:field_regex}
            `field` is the name of the variable/field that stores the
            substitution data, `field_regex` is a regular expression that is
            guaranteed to match the form of the substitution data, `line_regex`
            is an optional regex that will match the line the field is in.  If
            not given, all non-empty lines are matched (i.e. line_regex = `.+`)

        Rendering a file:
            A new rendering of the TemplateFile can be written after
            initializing data for all fields.  This is done with one of
            initData(), setField(), or passing the data dict directly to
            render() (see each method for details).

        Interpreting a file:
            To interpret a file, use the class factory method fromfile() to make
            a new initialized TemplateFile or read_file() for an existing,
            initialized TemplateFile.

        Example of creating and rendering new file:
            template_text = ""\"
            # Comment describing {filename[.*#.*]:[a-zA-Z0-9]+.dat}
            {resvar:resolution} = {resdata:[0-9]{2,4}}
            ""\"

            mytfile = TemplateFile(template_text)

            init_dict = {'filename': 'myfile.dat',
                'resvar' = 'resolution',
                'resdata' = '128'}

            mytfile.initData(init_dict)

        Example of loading in a file:
            template_text = ""\"
            # Comment describing {filename[.*#.*]:[a-zA-Z0-9]+.dat}
            {resvar:resolution} = {resdata:[0-9]{2,4}}
            ""\"

            # Assuming test.txt lines are 
            # "# Comment describing myfile.dat"
            # "resolution = 128",
            # then
            mytfile = fromfile('test.txt', template_text)
            # will yield a data dict with
            print(mytfile.getField('filename')) # myfile.dat
            print(mytfile.getField('resvar'))   # resolution
            print(mytfile.getField('resdata'))  # 128
        """
        #Key instance variables:
        #   self._template_text: The file's template text
        #   self._fields: Frozen set of the file fields.
        #   self._regexes: ordered mapping of _fields to (field_regex, line_regex)
        #Initialized here, but initially populated with None data:
        #   self._data: mapping of _fields to substitution data
        self._template_text = template_text
        self._fields, self._regexes = self._getFieldsAndRegs()
        self._data = {}
        for field in self._fields:
            self._data[field] = None

    def writeFile(self, savepath):
        """Write the file to the given full path."""
        from os.path import dirname
        from os import makedirs
        if dirname(savepath):
            makedirs(dirname(savepath), exist_ok=True)
        with open(savepath, 'w') as f:
            f.write(self.render())

    def setField(self, field, value):
        """Set `field` to store `value`."""
        if field not in self._fields:
            raise KeyError('{} is not a valid field for this TemplateFile!'.format(field))
        self._data[field] = value

    def getField(self, field):
        """Get the data stored in `field`."""
        if field not in self._fields:
            raise KeyError('{} is not a valid field for this TemplateFile!'.format(field))
        return self._data[field]

    def initData(self, data_dict):
        """Initialize the dictionary mapping fields to substitution data."""
        if data_dict.keys != self._fields:
            raise KeyError("data_dict keys do not match this TemplateFile's fields!")
        self._data = data_dict

    def render(self, data_dict=None):
        """Render the template into usable file text, return the text."""
        if self._data is None and data_dict is None:
            raise RuntimeError('TemplateFile data has not been initialized!')
        rendered_text = ""
        for line in self._template_text.splitlines(keepends=True):
            rendered_line = self._renderLine(line)
            rendered_text += rendered_line
        return rendered_text

    def _renderLine(self, line):
        """Render a single line."""
        if line.count('{') == 0:
            #No substitution descriptors, just render as is
            return line
        if line.count('}') < 1:
            raise ValueError('TemplateFile: Template text contains invalid line!')

        #Convert any substitution descriptors into valid format strings
        remove = False
        open_count = 0
        format_line = ""
        for i,c in enumerate(line):
            if c == '{':
                open_count += 1
            if c == '}':
                if open_count-1 == 0:
                    remove = False
                open_count -= 1
            if open_count > 0 and not remove:
                #Look for [ or :
                if c == '[' or c == ':':
                    remove = True
            if not remove:
                format_line += c

        return format_line.format(**self._data)

    def readFile(self, filepath):
        """Initialize data from file at `filepath`."""
        import re
        #NOTE: This algorithm makes use of the fact that fields are found in
        #   order, from the top to the bottom of the file.  It assumes data for
        #   all fields is available in the file.

        #If no fields, just return
        if len(self._fields) == 0:
            return

        #Build a stack to pop fields off of. TODO: is this inefficient?
        field_stack = []
        for field in self._regexes:
            field_regex, line_regex = self._regexes[field]
            field_stack.append((field, field_regex, line_regex))
        field_stack.reverse()

        #Iterate over lines in the file, searching for fields in order
        with open(filepath, 'r') as f:
            cur_field, cur_fregex, cur_lregex = field_stack.pop() #(field, field_regex, line_regex)
            fre = re.compile(cur_fregex)
            lre = re.compile(cur_lregex)
            found_all = False
            for line in f:
                lmatch = lre.match(line)
                if lmatch:
                    fmatch = fre.search(line)
                    #We use a while here to search for multiple fields on a
                    #single line. ASSUMPTION: all fields on a line have the
                    #same line_regex, if given
                    while fmatch:
                        field_data = line[fmatch.start():fmatch.end()]
                        self.setField(cur_field, field_data)
                        if len(field_stack) == 0:
                            found_all = True
                            break
                        cur_field, cur_fregex, cur_lregex = field_stack.pop()
                        fre = re.compile(cur_fregex)
                        lre = re.compile(cur_lregex)
                        fmatch = fre.search(line)
                if found_all:
                    break
       
        if not found_all:
            #We didn't find the current item, so add it back to the stack
            field_stack.insert(0,(cur_field,cur_fregex, cur_lregex))
            err_str = """All fields not found! Remaining fields in search order:
            {}""".format(field_stack)
            raise RuntimeError(err_str)

    @classmethod
    def fromfile(cls, filepath, template_text):
        """Factory method for creating a TemplateFile from an existing file."""
        ret = cls(template_text)
        ret.readFile(filepath)
        return ret

    def _getFieldsAndRegs(self):
        """Return fields and regexes in self._template_text.
        
        Parses self._template_text and returns a frozenset of fields as well as
        a mapping of those fields to their field regex and any line regex
            {<field_str>: (<field_regex>, <line_regex | None>)}"""
        from string import Formatter
        from collections import OrderedDict
        #TODO: Error checking
        fmt = Formatter()
        field_ret = []
        field_index = 1
        fregex_index = 2
        regex_ret = OrderedDict({})
        for parse_tuple in fmt.parse(self._template_text):
            field_text = parse_tuple[field_index]
            if field_text is None:
                continue
            line_regex = ".+"
            #Get the optional line_regex if provided
            #TODO maybe make sure user knows a literal '[' in field will break things
            if field_text.count('[') > 0:
                tokens = field_text.partition('[')
                field_text = tokens[0].strip()
                line_regex = tokens[2].rpartition(']')[0]
            field_ret.append(field_text)
            field_regex = parse_tuple[fregex_index]
            regex_ret[field_text] = (field_regex, line_regex)

        return frozenset(field_ret), regex_ret
