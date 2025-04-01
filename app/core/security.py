import bcrypt

if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__})