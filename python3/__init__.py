""" gdom : extensible DOM Implementation.
gdom provide a large DOM Implementation that get easily extended by third party.
Take a look at the GitHub project : https://github.com/YepoMax/gdom
"""

from gdom.implementation import DOMImplementation, DOMImplementationSource


# @author       Maximilien Smout
# @date         May 2014
# @version      0.1.0
# @credits      None
# @description  DOM Implementation Level 3
# @license      MIT
# @email        maximilien.smout@hotmail.com


"""

DOCTEST :
    Note : variable named 'nocare' will avoid object representation which may generate useless doctest error.

>>> from gdom import *
>>> DOMImp = DOMImplementation()
>>> doc = DOMImp.createDocument()
>>> root = doc.createElement("root")
>>> item = doc.createElement("item")
>>> itemNS = doc.createElementNS("http://namespaceURI.be/", "tag")
>>> # No prefix --> should be fixed at serialization
>>> root.setAttributeNS(XMLNS_URI, "xmlns:prefix", "http://namespaceURI.be/")
>>> nocare = item.appendChild(doc.createTextNode("text content"))
>>> nocare = itemNS.appendChild(doc.createCDATASection("<p> CDATASection </p>"))
>>> nocare = root.appendChild(item)
>>> nocare = root.appendChild(itemNS)
>>> nocare = doc.appendChild(root)
>>> nocare = DOMImp.getFeature("ls", "3.0")
>>> LSS = DOMImp.createLSSerializer()
>>> LSS.writeToString(doc)
'<root xmlns:prefix="http://namespaceURI.be/"><item>text content</item><prefix:tag><![CDATA[<p> CDATASection </p>]]></prefix:tag></root>'

"""

XMLNS_URI = "http://www.w3.org/2000/xmlns/"



if __name__ == "__main__":
    import doctest
    print(" Test starting ".center(40, "="), "\n")
    doctest.testfile("__init__.py")
    print("", " Test finished ".center(40, "="), sep="\n")
