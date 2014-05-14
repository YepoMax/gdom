gdom
====

IMPORTANT NOTE : DO NOT PAY ATTENTION TO THIS PROJECT - project is not open yet.
BUT : If you want to contribute to the project before I post first versions, contact me at maximilien.smout@hotmail.com

gdom provides a DOM (Level 3) implementation to Python that is intended to replace the built-in DOM implementation.
Being accurate (act as closely as possible as the DOM API described by W3C.org) and extensible is the main reason why gdom should be used instead of built-in DOM API.
This version of gdom only includes XML, LS and XPath but will later include a lot more DOM features.

gdom is a 'collaborative script' : anyone can contribute to both adding new DOM features and improving core scripts. If you want to join the train, please read the contribute.txt file to ensure your code matches with gdom specifications. Then, feel free to post your code here : [[url]].


How it defer with built-in
--------------------------

First difference is the features available.

Built-in DOM implementation provide the following features :

    * Core Level 1, Level 2 and basic Level 3;
    * XML Level 1, Level 2 and basic Level 3;
    * LS Level 3.
    
gdom implementation provide the following features :

    * Core Level 1, Level 2 and Level 3;
    * XML Level 1, Level 2 and Level 3;
    * LS Level 3;
    * XPath Level 3;
    * DTD (Document Type Definition);
    * More to come in the future.

Second difference is that gdom is designed to act ***exactly*** as W3C describe in their specifications, built-in dom doesn't. To see a full list of how Python' Built-in DOM doesn't respect W3C specifications, check here : [[url]]

Third (main) difference is that gdom is ***extensible*** : new features can easily be added by third-party. Plus, gdom is a 'collaborative script', everyone may submit an improvement to core scripts ([[url]]).


What is DOM
-----------

DOM (Document Object Model) is a platform and language-neutral API (Application Programming Interface) for valid HTML and well-formed XML documents. For more information, see : http://www.w3.org/TR/DOM-Level-3-Core/introduction.html


DOM Features
------------

DOM features are additionnal feature that can be loaded in your application through DOMImplementation.getFeature as describet by W3C (http://www.w3.org/TR/DOM-Level-3-Core/core.html#DOMFeatures).
w3c standard features can be found at http://www.w3.org/TR/ but here are the main one :

    [-] Core => included
    [-] XML => included
    [-] HTML *
    [-] LS => included
    [-] LS-Async (need Events feature to be added)
    [-] XPath => included
    [-] XLink
    [-] Traversal *
    [-] Range *
    [-] Validation *
    [-] Events
    
*Prior features.
