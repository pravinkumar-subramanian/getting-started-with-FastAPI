import re
from core.passwordlist import password as pwd_list
from difflib import SequenceMatcher
from itertools import groupby

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


def checkemail(email):
    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def checkpassword(password):
    regex = re.compile(
        r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z])\S{8,20}$")
    if re.fullmatch(regex, password):
        # check for character repetition in entire password
        for char in password:
            if password.count(char) > 5:
                raise ValueError(
                    'We do not allow a character to repeat more than five times in a password')
        # check for consecutive character repetition
        repetition_count = [len(list(j)) for _, j in groupby(password)]
        if max(repetition_count) > 2:
            raise ValueError(
                'Character repetition in password is beyond permissible limit')
        # check for most commonly used password
        for i in pwd_list:
            similarity = SequenceMatcher(
                None, i.lower(), password.lower()).ratio()
            if similarity >= 0.6:
                raise ValueError(
                    'Password not accepted because it follows most commonly used pattern/words')
        return True
    else:
        return False


# class to set UTC current timestamp for postgresql
class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
