# -*- coding: utf-8 -*-


class TestingClass(object):  # SHOULD FAIL
    pass


class TestingClass2(object):  # SHOULD PASS
    """"""


class TestingClass3(object):  # SHOULD PASS
    """
    Hola mundo
    """


class TestingClass4(object):  # SHOULD FAIL
    ""


class TestingClass5(object):  # SHOULD FAIL
    def foo(self):
        pass


class TestingClass6(object):  # SHOULD FAIL
    def foo(self):
        pass

    """Hola mundo"""


class TestingClass7(object):  # SHOULD FAIL

    """Hola mundo"""


class TestingClass8(object):  # SHOULD PASS
    """Hola mundo"""


class TestingClass9(object):  # SHOULD FAIL
    class TestingClass10(object):
        """Hola mundo"""


class TestingClass11(object):  # SHOULD PASS
    """Hola mundo"""
    class TestingClass12(object):
        """Hola mundo"""
