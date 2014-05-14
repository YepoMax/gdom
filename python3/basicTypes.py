from gdom.readonly import readonlyClass, readonlyMaster, ReadOnlyException



def itemInList(obj, i):
    """ Return item at index i if i < len(obj) else None """

    return obj[i] if abs(i) < len(obj) else None

def insertAt(_list, index, item, fill=None):
    """ Insert item in '_list' at specified 'index' and fill the rest with 'fill'. """
    if len(_list) < index:
        _list += [fill,]*(index - len(_list))
        _list.insert(index, item)



class DOMString(str):
    """
        str subclass that implements methods specified by W3C plus every methods defined in javascript.
        Methods from Java will be implemented in the future.
        This class is designed to easily implement javascript interpreter.
    """

    # Built-in
    def __add__(self, other): return DOMString(str.__add__(self, other))
    def __radd__(self, other): return DOMString(str.__radd__(self, other))
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

    # 'Javascript like' methods
    def charAt(self, i): return self[i]
    def charCodeAt(self, i): return ord(self[i])
    def contains(self, string): return string in self
    def concat(self, other): return DOMString(self + other)
    def indexOf(self, string): return self.find(string)
    #def lastIndexOf(self, string): return len(self) - len(string) - DOMString(self[-1::-1]).indexOf(string[-1::-1])
    def lastIndexOf(self, string): return self.rfind(string)
    def localeCompare(self, string):
        i = 0
        if self < string: i = -1
        elif self > string: i = 1
        return i
    def slice(self, start, end=None): return self[start:end]
    def substr(self, start, length): return self[start:start+length]
    def substring(self, start, end): return self[start if start > 0 else 0:end if end > 0 else 0]
    def toLowerCase(self): return self.lower()
    def toLocaleLowerCase(self): return self.lower() # No idea how to do it.
    def toUpperCase(self): return self.upper()
    def toLocaleUpperCase(self): return self.upper() # No idea how to achieve this ...
    def trim(self): return self.strip()
    def valueOf(self): return self
    def toString(self): return self
    @property
    def length(self): return len(self)
    @property
    def constructor(self): return type(self)

    def tagEnclose(self, tag, attributes={}):
        string = '<' + tag
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
    

    @property
    def length(self): return len(self)

    def __repr__(self): return "%s[ %s ]" % (type(self).__name__, list.__repr__(self)[1:-1])

class DOMStringList(OneTypeList):
    """ List of DOMString. """
    __slots__ = ()

    def __init__(self, *iterable, readonly=False): OneTypeList.__init__(self, *iterable, valueType=DOMString, readonly=readonly)




class NameList(OneTypeList):
    """ Provides an abstraction for an ordered collection of name and namespace value pairs. Items can be accessed by a 0-based index.
        This is used in 'validation' DOM feature (not implemented yet). """
    __slots__ = ()

    def __init__(self, *iterable, readonly=False): OneTypeList.__init__(self, *iterable, valueType=tuple, readonly=readonly)
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
