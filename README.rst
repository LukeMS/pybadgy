pybadgy
========
|travisci_badge|_

.. |travisci_badge| image:: https://travis-ci.org/LukeMS/pybadgy.svg?branch=master
.. _travisci_badge: https://travis-ci.org/LukeMS/pybadgy

Script to generate custom `shields.io`_-like badges.

.. _`shields.io`: https://shields.io/

How to use it
**************

Install `pybadgy` by either using pip:

.. code:: bash

    pip install git+https://github.com/LukeMS/pybadgy.git

or cloning the repo and building it:

.. code:: bash

    git clone https://github.com/LukeMS/pybadgy.git
    cd pybadgy
    python setup.py install

Do your stuff, obtain your stats, generate your badges:

.. code:: bash

    python -m pybadgy -f -o docs/badge1.svg -t pybadgy -v 25
    python -m pybadgy -f -o docs/badge2.svg -t doxygen -v 100
    python -m pybadgy -f -o docs/badge3.svg -t quality -v 60

Do that offline, using a continuous integration services, whatever. The following badges were created and deployed by my good friend Travis_:

|custom_badge1|_ |custom_badge2|_ |custom_badge3|_

.. |custom_badge1| image:: https://lukems.github.io/pybadgy/badge1.svg
.. _custom_badge1: https://lukems.github.io/pybadgy/badge1.svg
.. |custom_badge2| image:: https://lukems.github.io/pybadgy/badge2.svg
.. _custom_badge2: https://lukems.github.io/pybadgy/badge2.svg
.. |custom_badge3| image:: https://lukems.github.io/pybadgy/badge3.svg
.. _custom_badge3: https://lukems.github.io/pybadgy/badge3.svg
.. _Travis: https://travis-ci.org

Inspiration & sources
**********************

pybadgy started as a modified version of `coverage-badge`_ (`copyright notice`_), and probably still carries many lines of it's code. Thanks, Danilo Bargen!
The svg templates themselves are from shields.io.

.. _`coverage-badge`: https://github.com/dbrgn/coverage-badge
.. _`copyright notice`: LICENSE-coverage-badge

Motivation
***********

Some good and simple static code analysis tools like lcov and `doxy-coverage`_ should get their own badges. With pybadgy the only thing needed is to parse stuff and run a python script with label and value as arguments.

Let's say you already build you C/C++ documentation via Travis CI using Doxygen. Adding doxy-coverage+pybadgy and integrating the badge creation process to the job should now be trivial.

.. _`doxy-coverage`: https://github.com/alobbs/doxy-coverage

But other tools already do that...
*************************************

`openBadge`_ is an example of a great tool already doing custom badge creation. It requires, however, its own javascript framework which, as far as I know, Github Pages do not support.

Specific tools like `lcov2badge`_ also have requirements that prevent their use on static web servers like Github Pages.

shields.io can be used online and currently does a better job then pybadgy. But pybadgy can create badges offline.

.. _`openBadge`: https://github.com/lmarkus/openBadge
.. _`lcov2badge`: https://github.com/albanm/lcov2badge

TODO
*****

 * Support different value formats (only % so far);
 * Support different templates;
 * Include lcov parser;
 * Deploy wheel to pypi for proper pip installation.
