from copy import deepcopy
from re import match, sub as REsub
from gdom.readonly import readonlyClass, readonlyMaster, ReadOnlyException


### UTILS ============================================================================== ###

def itemInList(obj, i):
    """ Return item at index i if i < len(obj) else None """

    return obj[i] if abs(i) < len(obj) else None

def insertAt(_list, index, item, fill=None):
    """ Insert item in '_list' at specified 'index' and fill the rest with 'fill'. """
    if len(_list) < index:
        _list += [fill,]*(index - len(_list))
        _list.insert(index, item)

### ==================================================================================== ###



class DOMString(str):
    """
        str subclass that implements methods specified by W3C plus every methods defined in javascript.
        This class is designed to easily implement javascript interpreter.
    """

    # Notes :
    #
    # - DOMString.replace(old, new) will replace every occurence of old by new unlike specified in Javascript and Java where it only replaces the first occurence of old by new.
    #                           As consequence, replace and replaceAll acts the same way.
    # - Regexp are always given as Python regex (pattern string or RE objects).
    # - split method in Java takes a Capital letter (and become Split)
    #
    # Some methods in Java have the same name as Javascript methods but takes other arguments.
    # The function are made such as the method will act depending on what arguments are passed and return the appropriate result.
    #
    # Some methods won't raise exception while the Java/Javascript equivalent would
    # BUT no exception will be raised while the Java/Javascript equivalent wouldn't.

    # Built-in (redirect to DOMString type)
    def __add__(self, other): return DOMString(str.__add__(self, other))
    def __radd__(self, other): return DOMString(str.__add__(other, self))
    def __mul__(self, other): return DOMString(str.__mul__(self, other))
    def __rmul__(self, other): return DOMString(str.__rmul__(self, other))
    def __getitem__(self, key): return DOMString(str.__getitem__(self, key))
    def __mod__(self, other): return DOMString(str.__mod__(self, other))
    def __format__(self, f): return DOMString(str.__format__(self, f))
    # Redefine str methods to return DOMString type.
    def lower(self): return DOMString(str.lower(self))
    def upper(self): return DOMString(str.upper(self))
    def strip(self): return DOMString(str.strip(self))
    def rstrpi(self): return DOMString(str.rstrip(self))
    def format(self, *args, **kwdargs): return DOMString(str.format(self, *args, **kwdargs))
    def split(self, sep=None, maxsplit=-1): return [DOMString(s) for s in self.split(sep, maxsplit)]

    # 'Javascript like' methods
    def charAt(self, i): return self[i]
    def charCodeAt(self, i): return ord(self[i])
    def contains(self, string): return string in self
    def concat(self, other): return DOMString(self + other)
    def indexOf(self, string, fromIndex=0): return self[fromIndex:].find(string)
    #def lastIndexOf(self, string): return len(self) - len(string) - DOMString(self[-1::-1]).indexOf(string[-1::-1])
    def lastIndexOf(self, string, fromIndex=None): return (self[:fromIndex+1] if fromIndex else self).rfind(string)
    def localeCompare(self, string):
        i = 0
        if self < string: i = -1
        elif self > string: i = 1
        return i
    def slice(self, start, end=None): return self[start:end]
    def substr(self, start, length): return self[start:start+length]
    def substring(self, start, end): return self[start if start > 0 else 0:end if end > 0 else 0]
    def toLowerCase(self, locale={}): # See http://docs.oracle.com/javase/7/docs/api/java/lang/String.html#toLowerCase%28java.util.Locale%29 for explanation on locale argument.
        # No argument acts like Javascript's String.toLowerCase method.
        string = DOMString()
        for char in self:
            if char in locale: string += locale[char]
            else: string += char.lower()
        return string
    def toLocaleLowerCase(self): return self.lower() # No idea how to do it.
    def toUpperCase(self, locale={}): #See http://docs.oracle.com/javase/7/docs/api/java/lang/String.html#toUpperCase%28java.util.Locale%29 for explanation on locale argument
        # No argument acts like Javascript's String.toUpperCase method.
        string = DOMString()
        for char in self:
            if char in locale: string += locale[char]
            else: string += char.upper()
        return string
    def toLocaleUpperCase(self): return self.upper() # No idea how to achieve this ...
    def trim(self): return self.strip()
    def valueOf(obj, *args):
        """ Can be used as staticmethod. """
        if type(obj) is DOMString: value = obj
        elif type(obj) is str: value = DOMString(obj)
        elif type(obj) is bool: value = DOMString("True") if obj else DOMString("False")
        elif type(obj) is list:
            value, i = DOMString(), args[0] if len(args) else 0
            while (i < (args[0] + args[1] if len(args) else len(obj))) and (type(obj[i]) is str or type(obj[i]) is DOMString): value, i = value + obj[i], i + 1
            if i < len(obj): value = DOMString(repr(obj))
        else: value = DOMString(repr(obj))
        return value
    def toString(self): return self
    @property
    def length(self): return len(self)
    @property
    def constructor(self): return type(self)

    def tagEnclose(self, tag, attributes={}):
        string = DOMString('<') + tag
        for attr in attributes:
            string += ' %s="%s"' % (attr, str(attributes[attr]))
        return string + '>%s</%s>' % (self, tag)

    # HTML Wrapper methods
    # Note : the following methods doesn't return Node class, they all return DOMString type.
    def anchor(self, name="undefined"): return self.tagEnclose("a", {"name":name})
    def big(self): return self.tagEnclose("big") # <big> tag is not supported in HTML5
    def blink(self): return self.tagEnclose("blink") # blink tag is obsolete
    def bold(self): return self.tagEnclose("b")
    def fixed(self): return self.tagEnclose("tt") # <tt> tag is not supported in HTML5
    def fontcolor(self, color="undefined"): return self.tagEnclose("font", {"color": color}) # <font> tag is not supported in HTML5
    def fontsize(self, size="undefined"): return self.tagEnclose("font", {"size": size})
    def italic(self): return self.tagEnclose("i")
    def link(self, lk="undefined"): return '<a href="%s">%s</a>' % (lk, self)
    def small(self): return self.tagEnclose("small") # <small> tag is not supported in HTML5
    def strike(self): return self.tagEnclose("strike") # <strike> tag is not supported in HTML5
    def sub(self): return self.tagEnclose("sub")
    def sup(self): return self.tagEnclose("sup")

    # 'Java like' methods
    #def codePointAt(self, i): return self.charCodeAt(self, i)
    #def codePointBefore(self, i):
    def compareTo(self, string): return self.localeCompare(string)
    def compareToIgnoreCase(self, string): return self.lower().localeCompare(string.lower())
    def contentEquals(self, string): return self == string
    def startsWith(self, prefix, offset=0): return self[offset:offset+len(prefix)] == prefix
    def endsWith(self, suffix): return self.rfind(suffix) == len(self) - len(suffix) and self.rfind(suffix) > -1
    def equals(self, other): return self == other
    def equalsIgnoreCase(self, other): return self.lower() == other.lower()
    def getBytes(self, charset="utf-8"): return self.encode("utf-8")
    def getChars(self, srcBegin, srcEnd, dst, dstBegin):
        if srcBegin > srcEnd or srcBegin < 0 or srcEnd > len(self) or dstBegin < 0 or dstBegin + (srcEnd-srcBegin) > len(dst): raise IndexError("IndexOutOfBoundsException")
        for i in range(srcBegin, srcEnd): dst[dstBegin + (i-srcBegin)] = self[i]
    def hashCode(self): return hash(self)
    def isEmpty(self): return bool(self)
    def matches(self, pattern): return bool(match(pattern, self))
    def offsetByCodePoints(self, index, codePointOffset): return self.substr(index, codePointOffset)
    def regionMatches(self, *args): #ignoreCase, toffset, other, ooffset, length):
        if len(args) == 5: ignoreCase, toffset, other, ooffset, length = args
        elif len(args) == 4: ignoreCase, toffset, other, ooffset, length = (False,) + args
        else: raise TypeError("regionMatches() takes 4 or 5 arguments")
        return self.substr(toffset, length).equalsIgnoreCase( other[ooffset:ooffset+length] ) if ignoreCase else self.substr(toffset,length) == other[ooffset:ooffset+length]
    def replaceFirst(self, pattern, replacement): return REsub(pattern, replacement, self, 1)
    def Split(self, pattern, limit=0): return [DOMString(s) for s in REsub(pattern, " "*len(self), self, limit).split(" "*len(self))]
    def subSequence(self, start, end): return self[start:end]
    def toCharArray(self): return [c for c in self] # Will be list of str, not a list of DOMString
    def clone(self): return self # No need to perform self[:] since in Python strings are value types.
    def getClass(self): return self.__class__

    @staticmethod
    def copyValueOf(data, offset=0, count=None): return data[offset:count]
    # http://docs.oracle.com/javase/7/docs/api/java/lang/String.html

    # 'C like' methods
    def GetLength(self): return len(self)
    def IsEmpty(self): return bool(self)
    def GetAt(self, i): return self[i] if i >= 0 else None
    def Compare(self, string): return self.localeCompare(string)
    def CompareNoCase(self, string): return self.lower().localeCompare(string.lower())
    def Mid(self, start, count=None): return self.substr(start,count) if count else self[start:]
    def Left(self, count): return self[:count]
    def Right(self, count): return self[-count:]






### ======== TO DO ========= ###

class UserDataHandler:
    """ Not implemented yet """

    NODE_CLONED     = 1
    NODE_IMPORTED   = 2
    NODE_DELETED    = 3
    NODE_RENAMED    = 4
    NODE_ADOPTED    = 5


class DOMError:
    """ Not implemented yet """

    def __init__(self, name, message=""):

        self.name = name
        self.message = message

class DOMLocator:
    """ Not implemented yet """

    pass


### ======================== ###

### DOMConfig =================================== ###

def config_addParameter(DOMConfig, parameters):
    """ Customize a DOMConfiguration by adding new parameters. 'parameters' argument is a dictionary of parameters and their default value.
    Note :  DOMconfig is a DOMConfiguration object.
            'parameters' may include existing parameters, it will cause the parameters to have a new default value.
    """

    params = DOMConfig.parameterNames + [DOMString(p.lower()) for p in parameters if p not in DOMConfig.parameterNames]
    readonlyMaster.setAttr(DOMConfig, "parameterNames", params)

    for param, value in parameters.items(): DOMConfig.setParameter(param, value)

class DOMConfiguration(readonlyClass):
    """ Used at parsing, serializating, validation and normalization. """

    __parameters = {
        "canonical-form": False,
        "cdata-sections": True,
        "check-character-normalization": False,
        "comments": True,
        "datatype-normalization": False, # Note : Setting this parameter to True have no effect if "validate" is set to False.
        "element-content-whitespace": True,
        "entities": True,
        "error-handler": None,
        "infoset": None,
        "namespaces": True,
        "namespace-declarations": True,  # Note : This parameter have no effect if "namespaces" is set to False.
        "normalize-characters": False,
        "schema-location": None,    # Optional
        "schema-type": None,        # Optional
        "split-cdata-sections": True,
        "validate": False,
        "validate-if-schema": False,
        "well-formed": True
                    }

    __canonical = { "entities": False, "normalize-characters": False, "cdata-sections": False,
                    "namespaces": True, "namespace-declarations": True, "well-formed": True, "element-content-whitespace": True}
    __infoset = {   "validate-if-schema": False, "entities": False, "datatype-normalization": False, "cdata-sections": False,
                     "namespace-declarations": True, "well-formed": True, "element-content-whitespace": True, "comments": True, "namespaces": True}

    def __init__(self):

        readonlyMaster.setAttr(self, "parameterNames", DOMStringList( [DOMString(p) for p in self.__parameters], readonly=True ))

    def setParameter(self, name, value):
        """ Set parameter to value. Note 'name' should be one from DOMConfiguration.parameterNames. """

        name = name.lower()
        if name not in self.parameterNames: raise DOMException("NOT_FOUND_ERR", "Parameter '%s' is invalid" % name)

        # canonical-form
        if name == "canonical-form" and value: self.__parameters.update(self.__canonical)
        # datatype-normalization
        elif name == "datatype-normalization" and value: self.__parameters["validate"] = True
        # infoset
        elif name == "infoset" and value: self.__parameters.update(self.__infoset)
        # validate and validate-if-schema
        elif name == "validate" and value: self.__parameters["validate-if-schema"] = False
        elif name == "validate-if-schema" and value: self.__parameters["validate"] = False

        # canonical-form
        if name in self.__canonical and value != self.__canonical[name]: self.__parameters["canonical-form"] = False
        if name in self.__infoset and value != self.__infoset[name]: self.__parameters["infoset"] = False

        self.__parameters[name] = value

    def getParameter(self, name):
        """ Get parameter's value. """
        name = name.lower()
        if name not in self.parameterNames: raise DOMException("NOT_FOUND_ERR", "Parameter '%s' is invalid" % name)
        return self.__parameters[name]

    def canSetParameter(self, name):

        # Any parameter can be set, they're all implemented (or will all be implemented, if you're using beta)
        return name.lower() in self.parameterNames

    def __deepcopy__(self, *m):

        copied = DOMConfiguration()
        for param in self.parameterNames: config_addParameter( copied, self.__parameters )
        return copied

### ============================================= ###

class OneTypeList(list):
    """ Base class for lists that admit only 1 type.
        Subclasses of specified type are also allowed. """

    def __init__(self, *iterable, valueType=None, readonly=False, readonlyError=None):
        self.__readonly = False
        self.__readonlyError = readonlyError or ReadOnlyException("%s is readonly" % self.__class__.__name__)
        if valueType: self.__valueType = valueType
        elif len(iterable): self.__valueType = type(iterable[0])
        else: raise Exception
        list.__init__(self)
        for elem in iterable:
            if type(elem) != valueType and hasattr(elem, "__iter__"):
                for e in elem: self.append(e)
            #if type(elem) is not valueType: raise TypeError
            else: self.append(elem)
        self.__readonly = readonly
    def __getitem__(self, i): return list.__getitem__(self, i)
    def __setitem__(self, i, item): self.__checkReadonly(list.__setitem__, self, i, item)
    def __add__(self, other): return type(self)(OneTypeList(list.__add__(self, other), valueType=self.__valueType))
    def __mul__(self, other): return type(self)(OneTypeList(list.__mul__(self, other), valueType=self.__valueType))
    def __rmul__(self, other): return type(self)(OneTypeList(list.__rmul__(self, other), valueType=self.__valueType))
    def __iadd__(self, other): return type(self)(OneTypeList(list.__iadd__(self, other), valueType=self.__valueType))
    def __imul__(self, other): return type(self)(OneTypeList(list.__imul__(self, other), valueType=self.__valueType))

    def __checkReadonly(self, callback=None, *args):
        if self.__readonly: raise self.readonlyError
        if callback: callback(*args)
        return True

    def insert(self, i, item):
        if self.__readonly: raise self.__readonlyError
        if type(item) is not self.__valueType and not issubclass(type(item), self.__valueType): raise TypeError("Type <%s> doesn't match with required type <%s>." % (item.__class__.__name__, self.__valueType.__class__.__name__))
        list.insert(self, i, item)
    def append(self, item): self.insert(len(self), item)
    def clear(self): self.__checkReadonly(list.clear, self)
    def extend(self, iterable):
        for elem in iterable: self.append(elem)

    def contains(self, string): return string in self
    def item(self, i): return itemInList(self, i)
    def indexOf(self, item):
        i = len(self) - 1
        while i > -1 and self[i] != item: i-=1
        return i

    def __copy__(self): return type(self)([e for e in self], readonly=self.__readonly,readonlyError=self.__readonlyError)

    def __deepcopy__(self, memo): return type(self)([deepcopy(e)  for e in self], readonly=self.__readonly,readonlyError=self.__readonlyError)

    @property
    def length(self): return len(self)

    def __repr__(self): return "%s[ %s ]" % (type(self).__name__, list.__repr__(self)[1:-1])

class DOMStringList(OneTypeList):
    """ List of DOMString. """
    __slots__ = ()

    def __init__(self, *iterable, readonly=False, readonlyError=None): OneTypeList.__init__(self, *iterable, valueType=DOMString, readonly=readonly, readonlyError=readonlyError)





class NameList(OneTypeList):
    """ Provides an abstraction for an ordered collection of name and namespace value pairs. Items can be accessed by a 0-based index.
        This is used in 'validation' DOM feature (not implemented yet). """
    __slots__ = ()

    def __init__(self, *iterable, readonly=False, readonlyError=None): OneTypeList.__init__(self, *iterable, valueType=tuple, readonly=readonly, readonlyError=readonlyError)
    def __contains__(self, key): return key in dict(self)
    def contains(self, key): return key in self
    def getName(self, i):
        item = self.item(i)
        if item != None: item = item[1]
        return item
    def getNamespaceURI(self, i):
        item = self.item(i)
        if item != None: item = item[0]
        return item
