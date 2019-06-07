# -*- coding: utf-8 -*-


class TestingClass(object):  # SHOULD PASS
    """"""


class TestingClass1(object):  # SHOULD PASS
    """
    Hola mundo
    """


class TestingClass2(object):  # SHOULD PASS
    """Hola mundo"""


class TestingClass3(object):  # SHOULD PASS
    """Hola mundo"""
    class InternalTestingClass(object):
        """Hola mundo"""
